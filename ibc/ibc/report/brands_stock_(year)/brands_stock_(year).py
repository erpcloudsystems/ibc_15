# Copyright (c) 2024, erpcloud.systems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _

def execute(filters=None):
    if not filters:
        filters = {}
    columns = get_columns()
    data = get_data()
    return columns, data
def get_columns():
    columns=[
            {
                "label": "Brand",
                "fieldname": "brand",
                "fieldtype": "Link",
                "options": "Brand",
                "width": 150
            },]
    
    fiscal_years = frappe.get_all("Fiscal Year", fields=["name"], order_by="name ASC")
    for row in fiscal_years :
        columns.append(
               {
                "label": row.name,
                "fieldname": row.name,
                "fieldtype": "Currency",
                "width": 150
            }, 
        )
        
    return columns
    
def get_data():
    item_results = frappe.db.sql("""
        SELECT DISTINCT
            name as name
        FROM
            `tabBrand`
    """, as_dict=True)

    result = []
    if item_results:
        for item_dict in item_results:
            data = {
                'brand': item_dict.get('name'),
            }
            brands = item_dict.get('name')
            query = frappe.db.sql(f"""SELECT
                                        IFNULL(SUM(stock_value_difference), 0) AS res,
                                        `tabStock Ledger Entry`.fiscal_year AS year
                                        
                                    FROM
                                        `tabStock Ledger Entry` 
                                    WHERE
                                        `tabStock Ledger Entry`.brand = '{brands}'
                                        # AND `tabStock Ledger Entry`.fiscal_year  < year
                                        AND `tabStock Ledger Entry`.is_cancelled = 0
                                    GROUP BY
                                        year""", as_dict=True)
            total = 0.0
            for row in query:
                total += row.get('res')
                data[f"{row.get('year')}"] = total
            result.append(data)
    return result
