frappe.ui.form.on("Sales Order", {
	refresh(frm) {
		if (frm.is_new()) {
			// Whatever put a customer on this new doc - manual pick, "Make Sales Order"
			// from a Quotation, duplicating an old order, an import, ... - fill the
			// mobile no if it came through empty.
			if (frm.doc.customer && !frm.doc.custom_mobile_no) {
				set_mobile_no_for_customer(frm);
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

	customer(frm) {
		// Always overwrite on customer change - Frappe's own "fetch from" can leave
		// the previous customer's number in place when the field is permission
		// filtered out of its response (e.g. Customer.mobile_no is permlevel 1).
		set_mobile_no_for_customer(frm);
	},

	async validate(frm) {
		if (!frm.doc.custom_mobile_no) {
			await set_mobile_no_for_customer(frm);
		}

		if (!frm.doc.custom_mobile_no) {
			frappe.throw(
				__('لا يمكنك الاستمرار في أمر البيع هذا حتى تقوم بتعيين رقم الموبايل للعميل "{0}"', [
					frm.doc.customer_name || frm.doc.customer,
				])
			);
		}
	},
});

async function set_mobile_no_for_customer(frm) {
	if (!frm.doc.customer) return;

	// Calls a whitelisted method that ignores permissions/permlevel entirely,
	// instead of relying on the core "fetch from" (which silently drops
	// Customer.mobile_no for plain Sales Users).
	let r = await frappe.call({
		method: "ibc.ibc.utils.customer_contact.get_customer_mobile_no",
		args: { customer: frm.doc.customer },
	});
	frm.set_value("custom_mobile_no", r.message || "");
}