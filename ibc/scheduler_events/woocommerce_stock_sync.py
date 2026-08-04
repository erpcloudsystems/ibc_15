from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def sync_woocommerce_stock():
    """Every 3 minutes: recompute stock qty from Bin for every item that has a Website
    Item, and push any changed quantities to WooCommerce. Polls Bin directly instead of
    hooking a document event, since ERPNext writes Bin via raw SQL and never fires one."""
    from ibc.doctype_triggers.stock.item.item import sync_stock_qty

    item_codes = frappe.db.sql_list(
        "select distinct item_code from `tabWebsite Item` where item_code is not null"
    )
    for item_code in item_codes:
        sync_stock_qty(item_code)
