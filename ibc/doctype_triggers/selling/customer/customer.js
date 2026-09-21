frappe.ui.form.on("Customer", {
	refresh(frm) {
		// "Create > Customer" from a Lead pre-fills lead_name on the new, unsaved
		// form, but mobile_no (Read Only, fetched from lead_name.mobile_no) doesn't
		// reliably resolve on a mapped-doc load - fetch it explicitly so the number
		// is visible before the user even saves.
		if (frm.is_new() && frm.doc.lead_name && !frm.doc.mobile_no) {
			frappe.call({
				method: "ibc.doctype_triggers.selling.customer.customer.get_lead_mobile_no",
				args: { lead: frm.doc.lead_name },
			}).then((r) => {
				if (r.message) {
					frm.set_value("mobile_no", r.message);
				}
			});
		}
	},
});
