# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters, columns)
	return columns, data


def get_columns():
	return [
		{
			"label": _("Item"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 150
		},
		{
			"label": _("Item Name"),
			"fieldname": "item_name",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Brand"),
			"fieldname": "brand",
			"fieldtype": "Link",
			"options": "Brand",
			"width": 150
		},
		{
			"label": _("Item Group"),
			"fieldname": "item_group",
			"fieldtype": "Link",
			"options": "Item Group",
			"width": 150
		},
		{
			"label": _("Opening"),
			"fieldname": "opening",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Opening_v"),
			"fieldname": "opening_v",
			"fieldtype": "Float",
			"width": 150
		},
		{
			"label": _("Delivered"),
			"fieldname": "delivered",
			"fieldtype": "Float",
			"width": 150
		},
		{
			"label": _("Delivered_v"),
			"fieldname": "delivered_v",
			"fieldtype": "Float",
			"width": 150
		},
		{
			"label": _("Sales Return"),
			"fieldname": "sales_return",
			"fieldtype": "Float",
			"width": 150
		},
		{
			"label": _("Sales Return_v"),
			"fieldname": "sales_return_v",
			"fieldtype": "Float",
			"width": 150
		},
		{
			"label": _("Purchase"),
			"fieldname": "purchase",
			"fieldtype": "Float",
			"width": 150
		},
		{
			"label": _("Purchase_v"),
			"fieldname": "purchase_v",
			"fieldtype": "Float",
			"width": 150
		},
		{
			"label": _("Purchase Return"),
			"fieldname": "purchase_return",
			"fieldtype": "Float",
			"width": 150
		},
		{
			"label": _("Purchase Return_v"),
			"fieldname": "purchase_return_v",
			"fieldtype": "Float",
			"width": 150
		},
		{
			"label": _("Balance"),
			"fieldname": "balance",
			"fieldtype": "Float",
			"width": 150
		},
		{
			"label": _("Balance_v"),
			"fieldname": "balance_v",
			"fieldtype": "Float",
			"width": 150
		}
	]


def get_data(filters, columns):
	item_price_qty_data = []
	item_price_qty_data = get_item_price_qty_data(filters)
	return item_price_qty_data


def hash_query(filters, doctype, sum_of, conditions):
	return  frappe._dict(frappe.db.sql(
		"""
		select `tabStock Ledger Entry`.item_code, sum({sum_of}) as sum
				from `tabStock Ledger Entry`  join `tabWarehouse` on `tabWarehouse`.name = `tabStock Ledger Entry`.warehouse
				where `tabWarehouse`.summery_stock = 1
				and `tabStock Ledger Entry`.voucher_type = "{doctype}"
				and `tabStock Ledger Entry`.posting_date >= "{from_date}"
				and `tabStock Ledger Entry`.posting_date <= "{to_date}"
				and {conditions}
				and `tabStock Ledger Entry`.is_cancelled = 0
				GROUP BY `tabStock Ledger Entry`.item_code
		""".format(doctype=doctype, sum_of=sum_of, conditions=conditions, from_date= filters.get("from_date"), to_date=filters.get("to_date")) ))

def retransform(item_qty_in_allWarehouses1, item_valuationRate_in_allWarehouses1):
	body = {}
	for row in item_qty_in_allWarehouses1:
		body[row.item_code] = {
			"actual_qty": row.actual_qty,
		}
	for row in item_valuationRate_in_allWarehouses1:
		body[row.item_code]["valuation_rate"] =  row.valuation_rate

	return body
def get_item_price_qty_data(filters):

	item_results = frappe.db.sql("""
    SELECT distinct
			`tabItem`.name as item_code,
			`tabItem`.item_name as item_name,
			ifnull(`tabItem`.valuation_rate,0) as value,
			`tabItem`.brand as brand,
			`tabItem`.item_group as item_group
			from
			`tabItem`
		""", filters , as_dict=1)

	result = []
	delivered = hash_query(filters,"Delivery Note", "actual_qty", conditions = " `tabStock Ledger Entry`.actual_qty <0 ")
	delivered_v = hash_query(filters,"Delivery Note", "stock_value_difference", conditions = " `tabStock Ledger Entry`.actual_qty <0 ")
	sales_return = hash_query(filters,"Sales Invoice", "actual_qty", conditions = " `tabStock Ledger Entry`.actual_qty >0 ")
	purchase = hash_query(filters,"Purchase Invoice", "actual_qty", conditions = " `tabStock Ledger Entry`.actual_qty >0 ")
	purchase_return = hash_query(filters,"Purchase Invoice", "actual_qty", conditions = " `tabStock Ledger Entry`.actual_qty >0 ")
	item_qty_in_allWarehouses = frappe.db.sql("""select
							item_code,
							sum(actual_qty) as actual_qty
							from `tabStock Ledger Entry`
							WHERE `tabStock Ledger Entry`.posting_date <= "{from_date}"
							GROUP BY item_code""".format(from_date=filters.get("from_date")), as_dict=1)
	item_valuationRate_in_allWarehouses = frappe.db.sql("""select
							item_code,
							AVG(valuation_rate)  as valuation_rate
							from `tabStock Ledger Entry`
							WHERE `tabStock Ledger Entry`.posting_date <= "{from_date}"
							and `tabStock Ledger Entry`.is_cancelled = 0
							GROUP BY item_code""".format(from_date=filters.get("from_date")), as_dict=1)
	
	new_item_qty_in_allWarehouses = retransform(item_qty_in_allWarehouses, item_valuationRate_in_allWarehouses)

	item_qty_in_allWarehouses_balance_lessthan = frappe.db.sql("""select
							item_code,
							sum(actual_qty) as actual_qty
							from `tabStock Ledger Entry`
							WHERE `tabStock Ledger Entry`.posting_date <= "{to_date}"
							GROUP BY item_code""".format(to_date=filters.get("to_date")), as_dict=1)
	item_valuationRate_balance_allWarehouses = frappe.db.sql("""select
							item_code,
							AVG(valuation_rate)  as valuation_rate
							from `tabStock Ledger Entry`
							WHERE `tabStock Ledger Entry`.posting_date <= "{to_date}"
							and `tabStock Ledger Entry`.is_cancelled = 0
							GROUP BY item_code""".format(to_date=filters.get("to_date")), as_dict=1)
	sales_in_qty = frappe._dict(frappe.db.sql("""select
							item_code,
							SUM(actual_qty * valuation_rate) as sales_in_qty_value
							from `tabStock Ledger Entry`
							where 1 = 1
							and `tabStock Ledger Entry`.voucher_type = "Sales Invoice"
							and `tabStock Ledger Entry`.actual_qty >0
							and `tabStock Ledger Entry`.posting_date >= "{from_date}"
							and `tabStock Ledger Entry`.posting_date <= "{to_date}"
							and `tabStock Ledger Entry`.is_cancelled = 0
							GROUP BY `tabStock Ledger Entry`.item_code
							 """.format(from_date=filters.get("from_date"), to_date=filters.get("to_date"))))
	purchase_in_qty = frappe._dict(frappe.db.sql("""select
							item_code,
							SUM(actual_qty * valuation_rate) as purchase_in_qty_value
							from `tabStock Ledger Entry`
							where  `tabStock Ledger Entry`.voucher_type = "Purchase Invoice"
							and `tabStock Ledger Entry`.actual_qty >0
							and `tabStock Ledger Entry`.posting_date >= "{from_date}"
							and `tabStock Ledger Entry`.posting_date <= "{to_date}"
							and `tabStock Ledger Entry`.is_cancelled = 0
							GROUP BY `tabStock Ledger Entry`.item_code
							 """.format(from_date=filters.get("from_date"), to_date=filters.get("to_date"))))
	purchase_in_re_qty = frappe._dict(frappe.db.sql("""select
							item_code,
							SUM(actual_qty * valuation_rate) as purchase_in_re_qty_value
							from `tabStock Ledger Entry`
							where `tabStock Ledger Entry`.voucher_type = "Purchase Invoice"
							and `tabStock Ledger Entry`.actual_qty <0
							and `tabStock Ledger Entry`.posting_date >= "{from_date}"
							and `tabStock Ledger Entry`.posting_date <= "{to_date}"
							and `tabStock Ledger Entry`.is_cancelled = 0
							GROUP BY `tabStock Ledger Entry`.item_code
							 """.format(from_date=filters.get("from_date"), to_date=filters.get("to_date"))))
	new_item_qtybalance_in_allWarehouses = retransform(item_qty_in_allWarehouses_balance_lessthan, item_valuationRate_balance_allWarehouses)
	if item_results:
		for item_dict in item_results:
			data = {
				'brand': (item_dict.brand),
				'item_code': item_dict.item_code,
				'item_name': (item_dict.item_name),
				'delivered': delivered.get(item_dict.item_code),
				'delivered_v': delivered_v.get(item_dict.item_code),
				'sales_return': sales_return.get(item_dict.item_code),
				'purchase': purchase.get(item_dict.item_code),
				'purchase_return': purchase_return.get(item_dict.item_code),
				'item_group': (item_dict.item_group)
			}
			data['sales_return_v'] = sales_in_qty.get(item_dict.item_code)
			data['purchase_v'] = purchase_in_qty.get(item_dict.item_code)
			data['purchase_return_v'] = purchase_in_re_qty.get(item_dict.item_code)
			data['opening'] = new_item_qty_in_allWarehouses.get(item_dict.item_code)["actual_qty"] if new_item_qty_in_allWarehouses.get(item_dict.item_code) else new_item_qty_in_allWarehouses.get(item_dict.item_code)
			data['opening_v'] = new_item_qty_in_allWarehouses.get(item_dict.item_code).get("actual_qty") * new_item_qty_in_allWarehouses.get(item_dict.item_code).get("valuation_rate", 0) if new_item_qty_in_allWarehouses.get(item_dict.item_code) else new_item_qty_in_allWarehouses.get(item_dict.item_code)
			data['balance'] = new_item_qtybalance_in_allWarehouses.get(item_dict.item_code).get("actual_qty") if new_item_qtybalance_in_allWarehouses.get(item_dict.item_code) else 0
			data['balance_v'] = new_item_qtybalance_in_allWarehouses.get(item_dict.item_code).get("actual_qty") * new_item_qtybalance_in_allWarehouses.get(item_dict.item_code).get("valuation_rate", 0) if new_item_qtybalance_in_allWarehouses.get(item_dict.item_code) else 0
			result.append(data)

	return result



