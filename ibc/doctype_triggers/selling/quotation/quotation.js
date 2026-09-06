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

	validate(frm) {
		if (frm.doc.quotation_to === "Customer" && !frm.doc.custom_mobile_no) {
			frappe.throw(
				__('لا يمكنك الاستمرار في عرض السعر هذا حتى تقوم بتعيين رقم الموبايل للعميل "{0}"', [
					frm.doc.customer_name || frm.doc.party_name,
				])
			);
		}
	},
});
