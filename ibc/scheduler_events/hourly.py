from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def hourly():
    # Update valuation_rate from Bin to Item (only where different)
    frappe.db.sql("""
        UPDATE tabItem i
        INNER JOIN tabBin b ON i.name = b.item_code
        INNER JOIN tabWarehouse w ON w.name = b.warehouse
        SET i.valuation_rate = b.valuation_rate
        WHERE w.is_main_warehouse = 1 
        AND i.valuation_rate != b.valuation_rate
    """)
    
    # Sync brand from Item to Bin (only where different or NULL)
    frappe.db.sql("""
        UPDATE tabBin b
        INNER JOIN tabItem i ON i.name = b.item_code
        SET b.brand = i.brand
        WHERE b.brand != i.brand OR b.brand IS NULL
    """)
    
    # Update Quotation creator where NULL
    frappe.db.sql("""
        UPDATE tabQuotation 
        SET creator = owner 
        WHERE creator IS NULL
    """)
    
    # Sync item_group from Item to Bin (fixed join condition, only where different or NULL)
    frappe.db.sql("""
        UPDATE tabBin b
        INNER JOIN tabItem i ON i.name = b.item_code
        SET b.item_group = i.item_group
        WHERE b.item_group != i.item_group OR b.item_group IS NULL
    """)
    
    frappe.db.commit()
    