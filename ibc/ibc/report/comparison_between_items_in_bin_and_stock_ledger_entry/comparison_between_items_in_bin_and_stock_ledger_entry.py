# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe import msgprint, _
from frappe.utils import flt


def execute(filters=None):
	columns, data = [], []
	from_date = filters.get('from_date')
	to_date = filters.get('to_date')
	warehouse = filters.get('warehouse')
	columns = get_columns(filters)
	data = frappe.db.sql(f"""
			SELECT `tabItem`.name as name, `tabItem`.item_name as item_name,
				    `tabStock Ledger Entry`.warehouse as stockLE_warehouse
			FROM `tabItem`

			join `tabStock Ledger Entry` on `tabStock Ledger Entry`.item_code = `tabItem`.name


			WHERE `tabStock Ledger Entry`.warehouse = 'المخزن الرئيسي - IBC'
			and `tabStock Ledger Entry`.posting_date >= '2022-11-01'
			group by `tabItem`.name
	""",as_dict = 1)

	result = []
	for item_dict in data:

		qty_after_transaction = float(0)
		if frappe.db.exists("Stock Ledger Entry", {"item_code": item_dict.name, "warehouse": "المخزن الرئيسي - IBC"}):
			qty = frappe.get_last_doc('Stock Ledger Entry', filters={"item_code": item_dict.name, "warehouse" : "المخزن الرئيسي - IBC"})
			qty_after_transaction = qty.qty_after_transaction

			row = {
				'name' : item_dict.name,
				'item_name' : item_dict.item_name,
				'qty_after_transaction' : qty_after_transaction
			}
		result.append(row)
	return columns, result


def get_columns(filters):
	columns = [
		{
            "label": _("Item"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Item",
            "width": 100
        },
		{
            "label": _("Item Name"),
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 270
        },
		{
            "label": _("Bin Actual Qty"),
            "fieldname": "actual_qty",
            "fieldtype": "Data",
            "width": 100
        },
		{
            "label": _("Bin Warehouse"),
            "fieldname": "bin_warehouse",
            "fieldtype": "Link",
			"options": "Warehouse",
            "width": 200
        },
		{
            "label": _("Stock Ledger Entry Qty After Transaction"),
            "fieldname": "qty_after_transaction",
            "fieldtype": "float",
            "width": 200
        },
		{
            "label": _("Stock Ledger Entry Warehouse"),
            "fieldname": "stockLE_warehouse",
            "fieldtype": "Link",
			"options": "Warehouse",
            "width": 200
        },

	]
	return columns
