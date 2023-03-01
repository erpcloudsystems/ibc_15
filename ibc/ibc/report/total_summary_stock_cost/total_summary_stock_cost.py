# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _


def execute(filters=None):

	if not filters:
		filters = {}
	columns = get_columns()
	stock = get_total_stock(filters)

	return columns, stock


def get_columns():
	columns = [
		_("Company") + ":Link/Company:150",
		_("Warehouse") + ":Link/Warehouse:150",
		_("Item") + ":Link/Item:90",
		_("Item Name") + ":Data:250",
		_("Description") + "::300",
		_("Current Qty") + ":Float:100",
		_("Valuation Rate") + ":Float:100"
	]

	return columns


def get_total_stock(filters):
	conditions = ""
	columns = ""
	columnss = ""
	default_price_list = frappe.db.get_single_value('Selling Settings', 'selling_price_list')

	if filters.get("group_by") == "Warehouse":
		if filters.get("company"):
			conditions += " AND warehouse.company = %s" % frappe.db.escape(
				filters.get("company"), percent=False
			)

		conditions += " GROUP BY ledger.warehouse, item.item_code"
		columns += "'' as company, ledger.warehouse"
		columnss += "sum(ledger.actual_qty) as actual_qty,"
		columnss += "sum(ledger.valuation_rate)"
	else:
		conditions += " GROUP BY warehouse.company, item.item_code"
		columns += " warehouse.company, '' as warehouse"
		columnss += " (select sum(ledger.actual_qty) from `tabBin` AS ledger where ledger.item_code = item.item_code) as actual_qty "
		columnss += " ,(select sum(ledger.valuation_rate) from `tabBin` AS ledger where ledger.warehouse = 'المخزن الرئيسي - IBC' and ledger.item_code = item.item_code)"




	return frappe.db.sql(
		"""
			SELECT
				%s,
				item.item_code,
				item.item_name,
				item.description,
				%s
			FROM
				`tabBin` AS ledger
			INNER JOIN `tabItem` AS item
				ON ledger.item_code = item.item_code
			INNER JOIN `tabWarehouse` warehouse
				ON warehouse.name = ledger.warehouse
			INNER JOIN `tabItem Price` AS price
				ON ledger.item_code = price.item_code

			WHERE price.price_list = '{price_list}' %s""".format(price_list=default_price_list)
		% (columns,columnss, conditions)
	)
