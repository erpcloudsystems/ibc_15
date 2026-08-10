from __future__ import unicode_literals
import frappe
from frappe import _
from erpnext.stock.doctype.repost_item_valuation.repost_item_valuation import repost_entries

@frappe.whitelist()
def all():
    # Only repost if there are pending entries (reduces unnecessary processing)
    pending_count = frappe.db.count("Repost Item Valuation", {"status": "Queued"})
    if pending_count > 0:
        repost_entries()
    
    # Update summary_stock only for items that have bins in summary warehouses
    # Added WHERE clause to avoid updating items with no change
    frappe.db.sql("""
        UPDATE tabItem i
        SET i.summary_stock = (
            SELECT IFNULL(SUM(b.actual_qty), 0) 
            FROM tabBin b 
            JOIN tabWarehouse w ON b.warehouse = w.name 
            WHERE w.summery_stock = 1 AND b.item_code = i.name
        )
        WHERE EXISTS (
            SELECT 1 FROM tabBin b2 
            JOIN tabWarehouse w2 ON b2.warehouse = w2.name 
            WHERE w2.summery_stock = 1 AND b2.item_code = i.name
        )
    """)
    frappe.db.commit()