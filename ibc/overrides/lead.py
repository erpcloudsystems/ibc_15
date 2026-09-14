import frappe
from erpnext.crm.doctype.lead.lead import get_lead_details as _get_lead_details


@frappe.whitelist()
def get_lead_details(lead, posting_date=None, company=None, doctype=None):
	out = _get_lead_details(lead, posting_date=posting_date, company=company, doctype=doctype)

	if lead:
		out["system_type"] = frappe.db.get_value("Lead", lead, "system_type")

	return out
