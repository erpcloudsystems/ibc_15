# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe import msgprint, _
from frappe.utils import flt
from datetime import datetime


def execute(filters=None):
	columns, data = [], []
	from_date = filters.get('from_date')
	to_date = filters.get('to_date')
	warehouse = filters.get('warehouse')
	columns = get_columns(filters)
	data = frappe.db.sql(f"""
			SELECT  `tabBin`.item_code, `tabBin`.actual_qty, `tabBin`.warehouse
			FROM `tabBin`
			where `tabBin`.warehouse = 'المخزن الرئيسي - IBC'
	""",as_dict = 1)

	result = []

	for item_dict in data:
		q = float(0)
		if frappe.db.exists("Stock Ledger Entry", {"item_code": item_dict.item_code, "warehouse": 'المخزن الرئيسي - IBC', 'posting_date' : ['>', from_date]}):

			d = frappe.get_last_doc('Stock Ledger Entry', filters={"item_code": item_dict.item_code,
				"warehouse" : 'المخزن الرئيسي - IBC', 'posting_date' : ['>', from_date]})



		if d:
			q = d.qty_after_transaction



		row = {
			'name' : item_dict.item_code,
			'actual_qty' : item_dict.actual_qty,
			'warehouse' : item_dict.warehouse,
			'qty_after_transaction' : q,
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
            "label": _("Bin Actual Qty"),
            "fieldname": "actual_qty",
            "fieldtype": "Data",
            "width": 200
        },
		{
            "label": _("Warehouse"),
            "fieldname": "warehouse",
            "fieldtype": "Link",
			"options": "Warehouse",
            "width": 150
        },
		{
            "label": _("Stock Ledger Entry Qty After Transaction"),
            "fieldname": "qty_after_transaction",
            "fieldtype": "float",
            "width": 200
        },

	]
	return columns
