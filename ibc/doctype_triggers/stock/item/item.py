from __future__ import unicode_literals
import frappe
from frappe import _
from webshop.webshop.doctype.website_item.website_item import make_website_item
import json
import ast
import requests

@frappe.whitelist()
def before_insert(doc, method=None):
    pass
@frappe.whitelist()
def after_insert(doc, method=None):
    pass
@frappe.whitelist()
def onload(doc, method=None):
    pass
    # validation_rate_fetch(doc)
@frappe.whitelist()
def before_validate(doc, method=None):
    pass
@frappe.whitelist()
def validate(doc, method=None):
    pass
@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
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
