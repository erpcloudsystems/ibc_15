from __future__ import unicode_literals
import frappe
from frappe import _


def before_insert(doc, method=None):
    pass

def after_insert(doc, method=None):
    pass

def onload(doc, method=None):
    pass

def before_validate(doc, method=None):
    pass

def validate(doc, method=None):
    pass

def on_submit(doc, method=None):
    pass

def on_cancel(doc, method=None):
    pass

def on_update_after_submit(doc, method=None):
    pass

def before_save(doc, method=None):
    pass

def before_cancel(doc, method=None):
    pass

def on_update(doc, method=None):
    pass

def before_rename(doc, method, old, new, merge=False):
    if frappe.session.user == "Administrator":
        return

    roles = set(frappe.get_roles(frappe.session.user))
    if "Sales User" in roles and not roles & {"System Manager", "Sales Manager"}:
        frappe.throw(
            _("You are not permitted to edit the ID of this Quotation. Please contact your Sales Manager or System Manager."),
            frappe.PermissionError,
        )
