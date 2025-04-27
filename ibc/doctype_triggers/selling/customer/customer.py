from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def before_insert(doc, method=None):
    pass
@frappe.whitelist()
def after_insert(doc, method=None):
    if doc.lead_name:
        attachments = frappe.db.sql(
            """ Select file_name, file_url
                from `tabFile` where `tabFile`.attached_to_doctype = "Lead"
                and `tabFile`.attached_to_name = "{name}"
            """.format(name=doc.lead_name), as_dict=1)

        for x in attachments:
            file = frappe.get_doc({
            'doctype': 'File',
            'file_name': x.file_name,
            'file_url': x.file_url,
            'attached_to_doctype': 'Customer',
            'attached_to_name': doc.name
            })
            file.insert(ignore_permissions=True)

@frappe.whitelist()
def onload(doc, method=None):
    pass
@frappe.whitelist()
def before_validate(doc, method=None):
    pass
@frappe.whitelist()
def validate(doc, method=None):
    if doc.mobile_no:
        existing_customer = frappe.db.exists(
            "Customer",
            {
                "mobile_no": doc.mobile_no,
                "name": ["!=", doc.name]
            }
        )
        if existing_customer:
            frappe.throw(_("Mobile No already exists in another Customer: {0}").format(existing_customer))

@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
