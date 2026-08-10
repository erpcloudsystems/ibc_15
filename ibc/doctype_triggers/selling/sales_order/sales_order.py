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
