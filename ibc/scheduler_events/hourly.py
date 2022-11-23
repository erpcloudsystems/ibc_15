from __future__ import unicode_literals
import frappe
from frappe import _
import json, ast, requests
from requests_oauthlib import OAuth1

frappe.whitelist()
def hourly():
    pass
    '''
    frappe.db.sql(
        """update tabItem set tabItem.summary_stock = (select sum(tabBin.actual_qty) from tabBin join tabWarehouse on tabBin.warehouse = tabWarehouse.name where tabWarehouse.summery_stock = 1 and tabBin.item_code = tabItem.name)""")
    frappe.db.sql(
        """update tabItem inner join tabBin on tabItem.item_code = tabBin.item_code set tabItem.valuation_rate = tabBin.valuation_rate where tabBin.warehouse = "المخزن الرئيسي - IBC" and tabItem.valuation_rate != tabBin.valuation_rate""")
    frappe.db.sql(
        """ update tabItem join `tabWebsite Item` on tabItem.name = `tabWebsite Item`.item_code set `tabWebsite Item`.web_long_description = `tabItem`.discription_ar where tabItem.website_ar =1""")
    frappe.db.sql(
        """update tabBin inner join tabItem on tabItem.item_code = tabBin.item_code set tabBin.brand = tabItem.brand where tabItem.valuation_rate != 1000000112 """)
    frappe.db.sql(
        """update tabBin join tabItem on tabBin.item_code = tabItem.name set tabBin.item_group = tabItem.item_group""")
    frappe.db.sql(
        """update `tabSales Invoice` join `tabCustomer` set `tabSales Invoice`.c_sales_person = `tabCustomer`.sales_person where `tabSales Invoice`.c_sales_person is null""")
    frappe.db.sql(
        """update `tabSales Order` join `tabCustomer` set `tabSales Order`.c_sales_person = `tabCustomer`.sales_person where `tabSales Order`.c_sales_person is null""")
    frappe.db.sql(
        """update `tabDelivery Note Item` join `tabItem` on `tabDelivery Note Item`.item_code = `tabItem`.name set `tabDelivery Note Item`.brand = `tabItem`.brand""")
    frappe.db.sql(
        """update `tabDelivery Note Item` join `tabItem` on `tabDelivery Note Item`.item_code = `tabItem`.name set `tabDelivery Note Item`.item_group = `tabItem`.item_group""")
    frappe.db.sql(
        """update `tabPurchase Invoice Item` join `tabItem` on `tabPurchase Invoice Item`.item_code = `tabItem`.name set `tabPurchase Invoice Item`.brand = `tabItem`.brand""")
    frappe.db.sql(
        """update `tabPurchase Invoice Item` join `tabItem` on `tabPurchase Invoice Item`.item_code = `tabItem`.name set `tabPurchase Invoice Item`.item_group = `tabItem`.item_group""")
    frappe.db.sql(
        """update `tabPurchase Order Item` join `tabItem` on `tabPurchase Order Item`.item_code = `tabItem`.name set `tabPurchase Order Item`.brand = `tabItem`.brand""")
    frappe.db.sql(
        """update `tabPurchase Order Item` join `tabItem` on `tabPurchase Order Item`.item_code = `tabItem`.name set `tabPurchase Order Item`.item_group = `tabItem`.item_group""")
    frappe.db.sql(
        """update `tabPurchase Receipt Item` join `tabItem` on `tabPurchase Receipt Item`.item_code = `tabItem`.name set `tabPurchase Receipt Item`.brand = `tabItem`.brand""")
    frappe.db.sql(
        """update `tabPurchase Receipt Item` join `tabItem` on `tabPurchase Receipt Item`.item_code = `tabItem`.name set `tabPurchase Receipt Item`.item_group = `tabItem`.item_group""")
    frappe.db.sql(
        """update tabQuotation set tabQuotation.creator = tabQuotation.owner where tabQuotation.creator is null""")
    frappe.db.sql(
        """update `tabSales Invoice Item` join `tabItem` on `tabSales Invoice Item`.item_code = `tabItem`.name set `tabSales Invoice Item`.brand = `tabItem`.brand""")
    frappe.db.sql(
        """update `tabSales Invoice Item` join `tabItem` on `tabSales Invoice Item`.item_code = `tabItem`.name set `tabSales Invoice Item`.item_group = `tabItem`.item_group""")
    frappe.db.sql(
        """update `tabSales Order Item` join `tabItem` on `tabSales Order Item`.item_code = `tabItem`.name set `tabSales Order Item`.brand = `tabItem`.brand""")
    frappe.db.sql(
        """update `tabSales Order Item` join `tabItem` on `tabSales Order Item`.item_code = `tabItem`.name set `tabSales Order Item`.item_group = `tabItem`.item_group""")
    frappe.db.sql(
        """update `tabStock Ledger Entry` inner join tabItem on tabItem.item_code = `tabStock Ledger Entry`.item_code set `tabStock Ledger Entry`.brand = tabItem.brand where `tabStock Ledger Entry`.brand IS NULL""")
    frappe.db.sql(
        """update `tabStock Ledger Entry` join tabItem on `tabStock Ledger Entry`.item_code = tabItem.name set `tabStock Ledger Entry`.item_group = tabItem.item_group""")
    '''