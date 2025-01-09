# Copyright (c) 2025, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime

def execute(filters=None):
    columns = get_columns() 
    data = get_data(filters)
    return columns, data
def get_data(filters):
    con = ''
    if filters.get('sales_person'):
        con += f" AND `tabSales Team`.sales_person = '{filters.get('sales_person')}'"
    if filters.get('is_return'):
        con += " AND si.is_return = 1"
   
    to_date = filters.get('to_posting_date')
    if not to_date:
        frappe.throw("To Posting Date is required")

    # Parse to_date and from_date safely
    to_date = datetime.strptime(to_date, '%Y-%m-%d').date()

    from_date = filters.get('posting_date_from')
    if not from_date:
        frappe.throw("From Posting Date is required")
    from_date = datetime.strptime(from_date, '%Y-%m-%d').date()

    # Query data
    data = frappe.db.sql(f"""
    SELECT
        si.posting_date,
        `tabSales Invoice Item`.item_code,
        `tabSales Invoice Item`.item_name,
        SUM(
            CASE 
                WHEN si.is_return = 1 THEN ABS(`tabSales Invoice Item`.qty)
                ELSE `tabSales Invoice Item`.qty
            END
        ) AS total_qty,
        SUM(
            CASE 
                WHEN si.is_return = 1 THEN ABS(`tabSales Invoice Item`.amount)
                ELSE `tabSales Invoice Item`.amount
            END
        ) AS total_amount,
        `tabItem`.is_stock_item,
        `tabSales Invoice Item`.discount_percentage,
        `tabSales Team`.sales_person
    FROM 
        `tabSales Invoice` AS si
    LEFT JOIN 
        `tabSales Team` ON si.name = `tabSales Team`.parent
    LEFT JOIN 
        `tabSales Invoice Item` ON si.name = `tabSales Invoice Item`.parent
    LEFT JOIN 
        `tabItem` ON `tabSales Invoice Item`.item_code = `tabItem`.name
    WHERE 
        `tabItem`.is_stock_item = 1
        AND si.docstatus = 1
        AND si.posting_date BETWEEN '{from_date}' AND '{to_date}'
        {con}
    GROUP BY
        `tabSales Invoice Item`.item_code, `tabSales Team`.sales_person, `tabSales Invoice Item`.discount_percentage
    """, as_dict=True)

    # Filter data by date range (if needed)
    final_data = []
    for row in data:
        posting_date = row.get('posting_date')
        if posting_date:  
            if from_date <= posting_date <= to_date:  
                final_data.append(row)

    return final_data


def get_columns():
    return [
        {
            "fieldname": "item_code",
            "label": "Item Code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 250,
        },
        {
            "fieldname": "item_name",
            "label": "Item Name",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "total_qty",
            "label": "Total Quantity",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "total_amount",
            "label": "Total Amount",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "discount_percentage",
            "label": "Discount Percentage",
            "fieldtype": "Percent",
            "width": 90,
        },
        {
            "fieldname": "is_stock_item",
            "label": "Stock Item",
            "fieldtype": "Check",
            "width": 80,
        },
        {
            "fieldname": "sales_person",
            "label": "Sales Person",
            "fieldtype": "Link",
            "options": "Sales Person",
            "width": 200,
        },
    ]

