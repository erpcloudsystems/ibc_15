from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def before_insert(doc, method=None):
    pass
@frappe.whitelist()
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
@frappe.whitelist()
def onload(doc, method=None):
    pass
@frappe.whitelist()
def before_validate(doc, method=None):
    pass
@frappe.whitelist()
def validate(doc, method=None):
    pass
@frappe.whitelist()
def on_submit(doc, method=None):
    pass
@frappe.whitelist()
def on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
