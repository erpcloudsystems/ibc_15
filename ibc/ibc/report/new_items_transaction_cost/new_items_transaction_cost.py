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
			"fieldtype": "Float",
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



def get_item_price_qty_data(filters):
	conditions = ""
	conditions1 = ""
#vals = [filters.get("metal_ws") , filters.get("leather_ws") , filters.get("natural_ws") , filters.get("artificial_ws") , filters.get("metal_ws") , filters.get("supplier_ws") , filters.get("imported_ws")]


	item_results = frappe.db.sql("""
    SELECT distinct
			ifnull(`tabItem`.name,0) as item_code,
			ifnull(`tabItem`.item_name,0) as item_name,
			ifnull(`tabItem`.valuation_rate,0) as value,
			ifnull(`tabItem`.brand,0) as brand,
			ifnull(`tabItem`.item_group,0) as item_group,
			(ifnull((select sum(stock_value_difference)
				from `tabStock Ledger Entry` left join `tabWarehouse` on `tabWarehouse`.name = `tabStock Ledger Entry`.warehouse
				where `tabWarehouse`.summery_stock = 1
				and `tabStock Ledger Entry`.item_code = `tabItem`.item_code
				and `tabStock Ledger Entry`.voucher_type = "Delivery Note"
				and `tabStock Ledger Entry`.posting_date >= %(from_date)s
				and `tabStock Ledger Entry`.posting_date <= %(to_date)s
				and `tabStock Ledger Entry`.actual_qty <0
				and `tabStock Ledger Entry`.is_cancelled = 0),0)) as delivered_v,
			(ifnull((select sum(actual_qty)
				from `tabStock Ledger Entry` left join `tabWarehouse` on `tabWarehouse`.name = `tabStock Ledger Entry`.warehouse
				where `tabWarehouse`.summery_stock = 1
				and `tabStock Ledger Entry`.item_code = `tabItem`.item_code
				and `tabStock Ledger Entry`.voucher_type = "Delivery Note"
				and `tabStock Ledger Entry`.posting_date >= %(from_date)s
				and `tabStock Ledger Entry`.posting_date <= %(to_date)s
				and `tabStock Ledger Entry`.actual_qty <0
				and `tabStock Ledger Entry`.is_cancelled = 0),0)) as delivered,
			(ifnull((select sum(actual_qty)
				from `tabStock Ledger Entry` left join `tabWarehouse` on `tabWarehouse`.name = `tabStock Ledger Entry`.warehouse
				where `tabWarehouse`.summery_stock = 1
				and `tabStock Ledger Entry`.item_code = `tabItem`.item_code
				and `tabStock Ledger Entry`.voucher_type = "Sales Invoice"
				and `tabStock Ledger Entry`.posting_date >= %(from_date)s
				and `tabStock Ledger Entry`.posting_date <= %(to_date)s
				and `tabStock Ledger Entry`.actual_qty >0
				and `tabStock Ledger Entry`.is_cancelled = 0),0)) as sales_return,
			(ifnull((select sum(actual_qty)
				from `tabStock Ledger Entry` left join `tabWarehouse` on `tabWarehouse`.name = `tabStock Ledger Entry`.warehouse
				where `tabWarehouse`.summery_stock = 1
				and `tabStock Ledger Entry`.item_code = `tabItem`.item_code
				and `tabStock Ledger Entry`.voucher_type = "Purchase Invoice"
				and `tabStock Ledger Entry`.posting_date >= %(from_date)s
				and `tabStock Ledger Entry`.posting_date <= %(to_date)s
				and `tabStock Ledger Entry`.actual_qty >0
				and `tabStock Ledger Entry`.is_cancelled = 0),0)) as purchase,
			(ifnull((select sum(actual_qty)
				from `tabStock Ledger Entry` left join `tabWarehouse` on `tabWarehouse`.name = `tabStock Ledger Entry`.warehouse
				where `tabWarehouse`.summery_stock = 1
				and `tabStock Ledger Entry`.item_code = `tabItem`.item_code
				and `tabStock Ledger Entry`.voucher_type = "Purchase Invoice"
				and `tabStock Ledger Entry`.posting_date >= %(from_date)s
				and `tabStock Ledger Entry`.posting_date <= %(to_date)s
				and `tabStock Ledger Entry`.actual_qty <0
				and `tabStock Ledger Entry`.is_cancelled = 0),0)) as purchase_return
			from
			`tabItem`
		""", filters , as_dict=1)

	result = []
	if item_results:
		for item_dict in item_results:

			data = {
				'item_code': item_dict.item_code,
				'brand': (item_dict.brand),
				'item_name': (item_dict.item_name),
				'delivered': (item_dict.delivered),
				'delivered_v': (item_dict.delivered_v),
				'sales_return': (item_dict.sales_return),
				'purchase': (item_dict.purchase),
				'purchase_return': (item_dict.purchase_return),
				'item_group': (item_dict.item_group)
			}
			to_date = filters.get("to_date")
			from_date = filters.get("from_date")
			item = item_dict.item_code

			warehouses = frappe.db.sql("""select name as name from `tabWarehouse` where disabled = 0 """, as_dict=1)

			# Start getting all qty
			s = 0
			s1 = 0
			frat = 0
			s2 = 0
			frate = 0
			v_rate = 0
			sales_in_qty_value = 0
			purchase_in_qty_value = 0
			purchase_in_re_qty_value = 0
			for warehouse in warehouses:
				warehousee = warehouse.name
				opening = frappe.db.sql("""select
							qty_after_transaction as res,
							valuation_rate as frate
							from `tabStock Ledger Entry` join `tabWarehouse` on `tabStock Ledger Entry`.warehouse = `tabWarehouse`.name
							where
							`tabStock Ledger Entry`.item_code = %s
							and `tabStock Ledger Entry`.warehouse = %s
							and `tabStock Ledger Entry`.posting_date <= %s
							and `tabStock Ledger Entry`.is_cancelled = 0
							ORDER BY `tabStock Ledger Entry`.posting_date DESC, `tabStock Ledger Entry`.posting_time DESC , `tabStock Ledger Entry`.creation DESC LIMIT 1""",
										(item, warehousee, from_date), as_dict=1)
				for tqty in opening:
					s += tqty.res
					frat += tqty.res*tqty.frate


				balance = frappe.db.sql("""select
											qty_after_transaction as res,
											valuation_rate as frate
											from `tabStock Ledger Entry` join `tabWarehouse` on `tabStock Ledger Entry`.warehouse = `tabWarehouse`.name
											where
											`tabStock Ledger Entry`.item_code = %s
											and `tabStock Ledger Entry`.warehouse = %s
											and `tabStock Ledger Entry`.posting_date <= %s
											and `tabStock Ledger Entry`.is_cancelled = 0
											ORDER BY `tabStock Ledger Entry`.posting_date DESC, `tabStock Ledger Entry`.posting_time DESC , `tabStock Ledger Entry`.creation DESC LIMIT 1""",
										(item, warehousee, to_date), as_dict=1)
				for tqty in balance:
					s1 += tqty.res
					s2 += tqty.res * tqty.frate
					frate += tqty.frate

				sales_in_qty = frappe.db.sql("""select
							actual_qty as qty,
							valuation_rate as v_rate
							from `tabStock Ledger Entry` join `tabWarehouse` on `tabStock Ledger Entry`.warehouse = `tabWarehouse`.name
							where
							`tabStock Ledger Entry`.item_code = %s
							and `tabStock Ledger Entry`.voucher_type = "Sales Invoice"
							and `tabStock Ledger Entry`.actual_qty >0
							and `tabStock Ledger Entry`.warehouse = %s
							and `tabStock Ledger Entry`.posting_date >= %s
							and `tabStock Ledger Entry`.posting_date <= %s
							and `tabStock Ledger Entry`.is_cancelled = 0
							ORDER BY `tabStock Ledger Entry`.posting_date DESC, `tabStock Ledger Entry`.posting_time DESC , `tabStock Ledger Entry`.creation DESC """,
										(item, warehousee, from_date, to_date), as_dict=1)
				for qt in sales_in_qty:
					sales_in_qty_value += qt.qty * qt.v_rate

				purchase_in_qty = frappe.db.sql("""select
							actual_qty as qty,
							valuation_rate as v_rate
							from `tabStock Ledger Entry` join `tabWarehouse` on `tabStock Ledger Entry`.warehouse = `tabWarehouse`.name
							where
							`tabStock Ledger Entry`.item_code = %s
							and `tabStock Ledger Entry`.voucher_type = "Purchase Invoice"
							and `tabStock Ledger Entry`.actual_qty >0
							and `tabStock Ledger Entry`.warehouse = %s
							and `tabStock Ledger Entry`.posting_date >= %s
							and `tabStock Ledger Entry`.posting_date <= %s
							and `tabStock Ledger Entry`.is_cancelled = 0
							ORDER BY `tabStock Ledger Entry`.posting_date DESC, `tabStock Ledger Entry`.posting_time DESC , `tabStock Ledger Entry`.creation DESC """,
										(item, warehousee, from_date, to_date), as_dict=1)
				for qt in purchase_in_qty:
					purchase_in_qty_value += qt.qty * qt.v_rate

				purchase_in_re_qty = frappe.db.sql("""select
							actual_qty as qty,
							valuation_rate as v_rate
							from `tabStock Ledger Entry` join `tabWarehouse` on `tabStock Ledger Entry`.warehouse = `tabWarehouse`.name
							where
							`tabStock Ledger Entry`.item_code = %s
							and `tabStock Ledger Entry`.voucher_type = "Purchase Invoice"
							and `tabStock Ledger Entry`.actual_qty <0
							and `tabStock Ledger Entry`.warehouse = %s
							and `tabStock Ledger Entry`.posting_date >= %s
							and `tabStock Ledger Entry`.posting_date <= %s
							and `tabStock Ledger Entry`.is_cancelled = 0
							ORDER BY `tabStock Ledger Entry`.posting_date DESC, `tabStock Ledger Entry`.posting_time DESC , `tabStock Ledger Entry`.creation DESC """,
										(item, warehousee, from_date, to_date), as_dict=1)
				for qt in purchase_in_re_qty:
					purchase_in_re_qty_value += qt.qty * qt.v_rate

			data['purchase_v'] = purchase_in_qty_value
			data['sales_return_v'] = sales_in_qty_value
			data['purchase_return_v'] = purchase_in_re_qty_value
			data['opening'] = s
			data['opening_v'] = frat
			data['balance'] = s1
			data['balance_v'] = s2


			result.append(data)

	return result



