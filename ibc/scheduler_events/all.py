from __future__ import unicode_literals
import frappe
from frappe import _
from erpnext.stock.doctype.repost_item_valuation.repost_item_valuation import repost_entries

frappe.whitelist()
def all():
    repost_entries()

    bench --site egeu.erpcloud.systems execute erpnext.stock.doctype.repost_item_valuation.repost_item_valuation.repost_entries