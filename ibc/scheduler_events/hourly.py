from __future__ import unicode_literals
import frappe
from frappe import _
import json, ast, requests
from requests_oauthlib import OAuth1

frappe.whitelist()
def hourly():
    frappe.db.sql(
        """update tabItem inner join tabBin on tabItem.item_code = tabBin.item_code  join tabWarehouse on tabWarehouse.name = tabBin.warehouse set tabItem.valuation_rate = tabBin.valuation_rate where tabWarehouse.is_main_warehouse = 1 and tabItem.valuation_rate != tabBin.valuation_rate""")
    frappe.db.sql(
        """update tabBin inner join tabItem on tabItem.item_code = tabBin.item_code set tabBin.brand = tabItem.brand  """)
    frappe.db.sql(
        """update tabQuotation set tabQuotation.creator = tabQuotation.owner where tabQuotation.creator is null""")
    frappe.db.sql(
        """update tabBin join tabItem on tabBin.item_code = tabItem.name set tabBin.item_group = tabItem.item_group""")
    