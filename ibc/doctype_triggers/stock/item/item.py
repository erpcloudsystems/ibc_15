from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt
from webshop.webshop.doctype.website_item.website_item import make_website_item
import json
import ast
import requests

def before_insert(doc, method=None):
    pass

def after_insert(doc, method=None):
    pass

def onload(doc, method=None):
    pass
    # validation_rate_fetch(doc)

def before_validate(doc, method=None):
    pass

def validate(doc, method=None):
    pass

def before_save(doc, method=None):
    pass

def on_update(doc, method=None):
    website_item = frappe.db.get_value("Website Item", {"item_code": doc.name}, "name")
    if website_item:
        # Fetch the website item document
        website_item_doc = frappe.get_doc("Website Item", website_item)

        # Update the description_ar field
        website_item_doc.discription_ar = doc.discription_ar

        # Save changes to the website item
        website_item_doc.save(ignore_permissions=True)
# @frappe.whitelist()
# def validation_rate_fetch(doc):
#     if doc.get('name'):
#         if doc.get('item_defaults'):
#             default_warehouse = doc.item_defaults[0].default_warehouse if doc.item_defaults else None

#             # Proceed if a default warehouse is available and valuation_rate is not already set to 0
#             if default_warehouse:
#                 # Query the Bin table to get the valuation_rate where actual_qty is not zero
#                 bin_data = frappe.get_all('Bin', filters={
#                     'name': doc.item_code,
#                     'warehouse': default_warehouse,
#                     'actual_qty': ['!=', 0]
#                 }, fields=['valuation_rate'], limit=1)

#                 # If bin_data is found and valuation_rate is available, set it in the Item document
#                 if bin_data:
#                     bin_valuation_rate = bin_data[0].get('valuation_rate')
#                     if bin_valuation_rate:
#                         doc.valuation_rate = bin_valuation_rate
#                         doc.save()  # Save the document after setting the valuation_rate
#                         frappe.db.commit()  # Ensure changes are committed to the database


def get_stock_qty(item_code):
    """Total actual_qty for an item across all warehouses, read straight from Bin."""
    return flt(frappe.db.sql(
        "select sum(actual_qty) from `tabBin` where item_code=%s", item_code
    )[0][0])


def sync_stock_qty(item_code):
    """Recompute an item's stock qty from Bin and, if it changed, mirror it onto the
    Item/Website Item and push it to WooCommerce.

    Called every 3 minutes by ibc.scheduler_events.woocommerce_stock_sync (polling Bin
    directly, since ERPNext updates Bin via raw SQL and never fires document events on it).
    """
    try:
        stock_qty = get_stock_qty(item_code)

        if flt(frappe.db.get_value("Item", item_code, "custom_stock_qty")) != stock_qty:
            frappe.db.set_value("Item", item_code, "custom_stock_qty", stock_qty, update_modified=False)

        website_item = frappe.db.get_value(
            "Website Item", {"item_code": item_code}, ["name", "stock_qty"], as_dict=True
        )
        if not website_item or flt(website_item.stock_qty) == stock_qty:
            return

        frappe.db.set_value("Website Item", website_item.name, "stock_qty", stock_qty, update_modified=False)

        from ibc.doctype_triggers.stock.website_item.website_item import push_stock_qty
        frappe.enqueue(push_stock_qty, queue="short", website_item=website_item.name, stock_qty=stock_qty)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Item Stock Qty Sync Error")


@frappe.whitelist()
def bulk_publish_website_items(items):
    import json
    if isinstance(items, str):
        items = json.loads(items)

    published = []
    for item_name in items:
        doc = frappe.get_doc("Item", item_name)
        if not doc.published_in_website:
            website_item_name = make_website_item(doc)
            published.append([website_item_name, doc.item_name or item_name])
    return published
