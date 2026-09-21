const QUOTATION_MOBILE_NO_PARTY_TYPES = ["Customer", "Lead"];

frappe.ui.form.on("Quotation", {
	refresh(frm) {
		if (frm.is_new()) {
			// Whatever put a party on this new doc - manual pick, "Create Quotation"
			// from a Lead, duplicating an old quotation, an import, ... - fill the
			// mobile no if it came through empty.
			if (
				QUOTATION_MOBILE_NO_PARTY_TYPES.includes(frm.doc.quotation_to) &&
				frm.doc.party_name &&
				!frm.doc.custom_mobile_no
			) {
				set_mobile_no_for_party(frm);
			}
			return;
		}

		let roles = frappe.user_roles;
		let is_sales_user = roles.includes("Sales User");
		let can_override = roles.includes("System Manager") || roles.includes("Sales Manager");

		if (is_sales_user && !can_override) {
			frm.page.menu
				.find(".menu-item-label:contains('" + __("Rename") + "')")
				.closest("li")
				.remove();
		}
	},

	party_name(frm) {
		// Always overwrite on party change - Frappe's own "fetch from" can leave
		// the previous party's number in place when the field is permission
		// filtered out of its response (e.g. Customer.mobile_no is permlevel 1).
		set_mobile_no_for_party(frm);
	},

	async validate(frm) {
		if (!QUOTATION_MOBILE_NO_PARTY_TYPES.includes(frm.doc.quotation_to)) return;

		if (!frm.doc.custom_mobile_no) {
			await set_mobile_no_for_party(frm);
		}

		if (!frm.doc.custom_mobile_no) {
			frappe.throw(
				__('لا يمكنك الاستمرار في عرض السعر هذا حتى تقوم بتعيين رقم الموبايل للعميل "{0}"', [
					frm.doc.customer_name || frm.doc.party_name,
				])
			);
		}
	},
});

async function set_mobile_no_for_party(frm) {
	if (!QUOTATION_MOBILE_NO_PARTY_TYPES.includes(frm.doc.quotation_to) || !frm.doc.party_name) {
		return;
	}

	// Calls a whitelisted method that ignores permissions/permlevel entirely,
	// instead of relying on the core "fetch from" (which silently drops
	// Customer.mobile_no for plain Sales Users) or reading the Lead/Customer
	// directly (some Sales Users are restricted from a Lead by a "Sales Person"
	// user permission).
	let r = await frappe.call({
		method: "ibc.doctype_triggers.selling.quotation.quotation.get_party_mobile_no",
		args: { quotation_to: frm.doc.quotation_to, party_name: frm.doc.party_name },
	});
	frm.set_value("custom_mobile_no", r.message || "");
}
