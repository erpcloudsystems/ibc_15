from __future__ import unicode_literals
import frappe
from frappe import _
import json, ast, requests
from requests_oauthlib import OAuth1

frappe.whitelist()
def hourly():
    frappe.db.sql(
        """update tabItem set tabItem.summary_stock = (select sum(tabBin.actual_qty) from tabBin join tabWarehouse on tabBin.warehouse = tabWarehouse.name where tabWarehouse.summery_stock = 1 and tabBin.item_code = tabItem.name)""")
    frappe.db.sql(
        """update tabItem inner join tabBin on tabItem.item_code = tabBin.item_code set tabItem.valuation_rate = tabBin.valuation_rate where tabBin.warehouse = "المخزن الرئيسي - IBC" and tabItem.valuation_rate != tabBin.valuation_rate""")
    frappe.db.sql(
        """ update tabItem join `tabWebsite Item` on tabItem.name = `tabWebsite Item`.item_code set `tabWebsite Item`.web_long_description = `tabItem`.discription_ar where tabItem.website_ar =1""")
