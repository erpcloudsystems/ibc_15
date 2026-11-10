from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def sync_customer_system_type():
	"""Manual sync (not scheduled): pulls System Type from each Customer's linked
	Lead (lead_name) into Customer.system_type. Customer.system_type only refreshes
	via fetch_from when the Customer document itself is saved, so if a Lead's
	System Type changes after conversion, the Customer (and anything that fetches
	from it, e.g. Sales Invoice.custom_system_type) goes stale until someone runs
	this. Run manually with:
	bench --site <site> execute ibc.scheduler_events.sync_customer_system_type.sync_customer_system_type

	DISABLED for now — body commented out below. Uncomment to re-enable.
	"""
	# frappe.db.sql("""
	# 	UPDATE `tabCustomer` c
	# 	JOIN `tabLead` l ON l.name = c.lead_name
	# 	SET c.system_type = l.system_type
	# 	WHERE c.lead_name IS NOT NULL AND c.lead_name != ''
	# 	  AND l.system_type IS NOT NULL AND l.system_type != ''
	# 	  AND (c.system_type IS NULL OR c.system_type != l.system_type)
	# """)
	# frappe.db.commit()
	pass
