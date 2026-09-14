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

	let r = await frappe.db.get_value("Customer", frm.doc.party_name, "lead_name");
	let lead = r.message && r.message.lead_name;
	if (!lead) return;

	let r2 = await frappe.db.get_value("Lead", lead, "mobile_no");
	let mobile_no = r2.message && r2.message.mobile_no;
	if (mobile_no) {
		frm.set_value("custom_mobile_no", mobile_no);
	}
}
