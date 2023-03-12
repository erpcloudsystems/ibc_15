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
		_("Item Group") + ":Data:250",
		_("Description") + "::300",
		_("Current Qty") + ":Float:100",
		_("Price List Rate") + ":Currency:120"
	]

	return columns


def get_total_stock(filters):
	conditions = ""
	columns = ""
	default_price_list = frappe.db.get_single_value('Selling Settings', 'selling_price_list')

	if filters.get("group_by") == "Warehouse":
		if filters.get("company"):
			conditions += " AND warehouse.company = %s" % frappe.db.escape(
				filters.get("company"), percent=False
			)

		conditions += " GROUP BY ledger.warehouse, item.item_code"
		columns += "'' as company, ledger.warehouse"
	else:
		conditions += " GROUP BY warehouse.company, item.item_code"
		columns += " warehouse.company, '' as warehouse"

	return frappe.db.sql(
		"""
			SELECT
				%s,
				item.item_code,
				item.item_name,
				item.item_group,
				item.description,
				sum(ledger.actual_qty) as actual_qty,
				price.price_list_rate
			FROM
				`tabBin` AS ledger
			INNER JOIN `tabItem` AS item
				ON ledger.item_code = item.item_code
			INNER JOIN `tabWarehouse` warehouse
				ON warehouse.name = ledger.warehouse
			INNER JOIN `tabItem Price` AS price
				ON ledger.item_code = price.item_code

			WHERE
				warehouse.summery_stock = 1
				and price.price_list = '{price_list}' %s""".format(price_list=default_price_list)
		% (columns, conditions)
	)
