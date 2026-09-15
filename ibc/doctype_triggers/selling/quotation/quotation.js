frappe.ui.form.on("Quotation", {
	refresh(frm) {
		if (frm.is_new()) return;

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
		fill_mobile_no_from_lead(frm);
	},

	async validate(frm) {
		if (frm.doc.quotation_to !== "Customer") return;

		await fill_mobile_no_from_lead(frm);

		if (!frm.doc.custom_mobile_no) {
			frappe.throw(
				__('لا يمكنك الاستمرار في عرض السعر هذا حتى تقوم بتعيين رقم الموبايل للعميل "{0}"', [
					frm.doc.customer_name || frm.doc.party_name,
				])
			);
		}
	},
});

async function fill_mobile_no_from_lead(frm) {
	if (frm.doc.quotation_to !== "Customer" || frm.doc.custom_mobile_no || !frm.doc.party_name) {
		return;
	}

	// Calls a whitelisted method (gated on Customer read access) instead of
	// reading the Lead directly - some Sales Users can see the Customer but
	// are restricted from the Lead by a "Sales Person" user permission.
	let r = await frappe.call({
		method: "ibc.doctype_triggers.selling.quotation.quotation.get_customer_mobile_no",
		args: { customer: frm.doc.party_name },
	});
	if (r.message) {
		frm.set_value("custom_mobile_no", r.message);
	}
}
