from __future__ import unicode_literals
import frappe
from frappe import _
from ibc.ibc.utils.mobile_no_duplicate import validate_unique_mobile_no


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
    validate_unique_mobile_no(doc)
    if doc.status == "Open" and not doc.notes:
        frappe.throw(_("Please add notes to the lead"))

@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
def before_rename(doc, method, old, new, merge=False):
    if frappe.session.user == "Administrator":
        return

    roles = set(frappe.get_roles(frappe.session.user))
    if "Sales User" in roles and not roles & {"System Manager", "Sales Manager"}:
        frappe.throw(
            _("You are not permitted to edit the ID of this Lead. Please contact your Sales Manager or System Manager."),
            frappe.PermissionError,
        )
