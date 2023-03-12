from __future__ import unicode_literals
import frappe
from frappe import _
from erpnext.stock.doctype.repost_item_valuation.repost_item_valuation import repost_entries

frappe.whitelist()
def all():
    repost_entries()
    frappe.db.sql("""
    update tabItem set tabItem.summary_stock = (select sum(tabBin.actual_qty) from tabBin join tabWarehouse on tabBin.warehouse = tabWarehouse.name where tabWarehouse.summery_stock = 1 and tabBin.item_code = tabItem.name) 
    """)