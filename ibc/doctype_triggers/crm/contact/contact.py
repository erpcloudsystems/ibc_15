from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def before_insert(doc, method=None):
    pass
@frappe.whitelist()
def after_insert(doc, method=None):
    pass
@frappe.whitelist()
def onload(doc, method=None):
    pass
@frappe.whitelist()
def before_validate(doc, method=None):
    pass
@frappe.whitelist()
def validate(doc, method=None):
    if doc.mobile_no:
        existing_contact = frappe.db.exists(
            "Contact",
            {
                "mobile_no": doc.mobile_no,
                "name": ["!=", doc.name]
            }
        )
        if existing_contact:
            frappe.throw(_("Mobile No already exists in another Contact: {0}").format(existing_contact))
    if doc.phone:
        existing_contact = frappe.db.exists(
            "Contact",
            {
                "phone": doc.phone,
                "name": ["!=", doc.name]
            }
        )
        if existing_contact:
            frappe.throw(_("Phone already exists in another Contact: {0}").format(existing_contact))      
@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
