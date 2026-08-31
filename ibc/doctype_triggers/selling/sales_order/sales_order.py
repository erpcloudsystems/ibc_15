from __future__ import unicode_literals
import frappe
from frappe import _


def before_insert(doc, method=None):
    pass

def after_insert(doc, method=None):
    pass
    ### share sales order contain item with brand Honeywell * ###
    # flag = False
    # for row in doc.items:
    #     if row.brand == "Honeywell *":
    #         flag = True
    # if flag:
    #     ## create docshare 
    #     docshare = frappe.get_doc({
    #         "doctype":"DocShare",
    #         "user":"alaa@ibcegypt.com",
    #         "read":1,
    #         "share_name":doc.name,
    #         "share_doctype":"Sales Order"
    #         })
    #     docshare.insert(ignore_permissions = True)
    #     frappe.db.commit()
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
            _("You are not permitted to edit the ID of this Sales Order. Please contact your Sales Manager or System Manager."),
            frappe.PermissionError,
        )
