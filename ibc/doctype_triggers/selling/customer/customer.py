from __future__ import unicode_literals
import frappe
from frappe import _


def before_insert(doc, method=None):
    pass

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

def onload(doc, method=None):
    pass

def before_validate(doc, method=None):
    pass

def validate(doc, method=None):
    if doc.mobile_no and not doc.lead_name:
        existing_lead = frappe.db.exists(
            "Lead",
            {
                "mobile_no": doc.mobile_no
            }
        )
        if existing_lead:
            frappe.throw(_("Mobile No already exists in Lead: {0}").format(existing_lead))

def before_save(doc, method=None):
    pass

def on_update(doc, method=None):
    pass
