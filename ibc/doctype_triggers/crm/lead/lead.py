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
        existing_lead = frappe.db.exists(
            "Lead",
            {
                "mobile_no": doc.mobile_no,
                "name": ["!=", doc.name]
            }
        )
        if existing_lead:
            frappe.throw(_("Mobile No already exists in another Lead: {0}").format(existing_lead))
    if doc.status == "Open" and not doc.notes:
        frappe.throw(_("Please add notes to the lead"))

@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
