from __future__ import unicode_literals
import frappe
from ibc.ibc.utils.mobile_no_duplicate import validate_unique_mobile_no
from ibc.ibc.utils.customer_contact import sync_customer_mobile_no


def before_insert(doc, method=None):
    pass

@frappe.whitelist()
def get_lead_mobile_no(lead):
    """Whitelisted for the client script - lets the new, unsaved Customer form
    (opened via "Create > Customer" on a Lead) show the number immediately."""
    return frappe.db.get_value("Lead", lead, "mobile_no")

def after_insert(doc, method=None):
    if doc.lead_name:
        # Fixed: Use parameterized query to prevent SQL injection
        attachments = frappe.db.sql("""
            SELECT file_name, file_url
            FROM `tabFile`
            WHERE attached_to_doctype = 'Lead'
            AND attached_to_name = %s
        """, (doc.lead_name,), as_dict=1)

        for x in attachments:
            file = frappe.get_doc({
            'doctype': 'File',
            'file_name': x.file_name,
            'file_url': x.file_url,
            'attached_to_doctype': 'Customer',
            'attached_to_name': doc.name
            })
            file.insert(ignore_permissions=True)

        if not doc.customer_primary_contact:
            # Customer.mobile_no already fetches from lead_name.mobile_no (site-level
            # Property Setter) and is populated by this point, but that alone doesn't
            # create/link an actual Contact - do that too, so customer_primary_contact
            # and Contact Phone are consistent with it (other logic, incl. Quotation/
            # Sales Order, looks up the Contact, not just the raw field).
            mobile_no = doc.mobile_no or frappe.db.get_value("Lead", doc.lead_name, "mobile_no")
            if mobile_no:
                sync_customer_mobile_no(doc.name, mobile_no)

def onload(doc, method=None):
    pass

def before_validate(doc, method=None):
    pass

def validate(doc, method=None):
    validate_unique_mobile_no(doc)

def before_save(doc, method=None):
    pass

def on_update(doc, method=None):
    pass
