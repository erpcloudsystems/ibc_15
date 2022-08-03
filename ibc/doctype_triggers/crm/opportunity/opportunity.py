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
     frappe.db.sql(
        """update tabItem set tabItem.summary_stock = (select sum(tabBin.actual_qty) from tabBin join tabWarehouse on tabBin.warehouse = tabWarehouse.name where tabWarehouse.summery_stock = 1 and tabBin.item_code = tabItem.name)""")
    
@frappe.whitelist()
def validate(doc, method=None):
    pass
@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
