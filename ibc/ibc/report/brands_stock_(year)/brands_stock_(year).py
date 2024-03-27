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
        return [
            {
                "label": "Brand",
                "fieldname": "brand",
                "fieldtype": "Link",
                "options": "Brand",
                "width": 150
            },
            {
                "label": "2019",
                "fieldname": "2019",
                "fieldtype": "Currency",
                "width": 150
            },
            {
                "label":"2020",
                "fieldname": "2020",
                "fieldtype": "Currency",
                "width": 150
            },
            {
                "label": "2021",
                "fieldname": "2021",
                "fieldtype": "Currency",
                "width": 150
            },
            {
                "label": "2022",
                "fieldname": "2022",
                "fieldtype": "Currency",
                "width": 150
            },
            {
                "label": "2023",
                "fieldname": "2023",
                "fieldtype": "Currency",
                "width": 150
            },
            {
                "label": "2024",
                "fieldname": "2024",
                "fieldtype": "Currency",
                "width": 150
            },
		    ]
    
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
                                        `tabFiscal Year`.name AS year
                                        
                                    FROM
                                        `tabStock Ledger Entry` 
                                    LEFT JOIN `tabFiscal Year` ON `tabStock Ledger Entry`.fiscal_year = `tabFiscal Year`.name
                                    WHERE
                                        `tabStock Ledger Entry`.brand = '{brands}'
                                        # AND `tabStock Ledger Entry`.YEAR(posting_date)  < year
                                        AND `tabStock Ledger Entry`.is_cancelled = 0
                                    GROUP BY
                                        `tabFiscal Year`.name""", as_dict=True)
            for row in query:
                data[f"{row.get('year')}"] = row.get('res')
            result.append(data)
    return result
