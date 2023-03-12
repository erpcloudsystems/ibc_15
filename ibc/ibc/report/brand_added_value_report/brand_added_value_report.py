# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []

	data = get_data(filters)
	columns = get_columns()

	return columns, data

def get_data(filters):
	from_date = filters.get('from_date')
	to_date = filters.get('to_date')
	purchase_in_qty_value = 0
#  or name = 'Farfisa' or name = 'Honeywe'
	result = []
	brand = frappe.db.sql("""
		select name as name
		from `tabBrand`
		""",as_dict= 1)
	for b in brand:
		item_results = frappe.db.sql(f"""
    	SELECT distinct
			ifnull(`tabItem`.name,0) as item_code,
			ifnull(`tabItem`.item_name,0) as item_name,
			ifnull(`tabItem`.valuation_rate,0) as value,
			ifnull(`tabItem`.brand,0) as brand,
			ifnull(`tabItem`.item_group,0) as item_group,
			ifnull((select sum(amount)
				from `tabPurchase Invoice Item`
				join `tabPurchase Invoice` on `tabPurchase Invoice`.name = `tabPurchase Invoice Item`.parent
			where `tabPurchase Invoice Item`.brand = '{b.name}'
			and `tabPurchase Invoice`.posting_date between '{from_date}' and '{to_date}'
			and `tabPurchase Invoice`.docstatus = 1), 0) as purchase,

			ifnull((select sum(amount)
				from `tabSales Invoice Item`
				join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent
			where `tabSales Invoice Item`.brand = '{b.name}'
			and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'
			and `tabSales Invoice`.docstatus = 1), 0) as sales
			from
			`tabItem`
			where `tabItem`.brand = '{b.name}'
		""" , as_dict=1)
		frat = 0
		s = 0
		current_value = 0
		sales_value = 0
		cogs = 0
		added_value = 0
		if item_results:
			for item_dict in item_results:

				data = {
					'brand': (b.name),
					'purchase' : item_dict.purchase,
					'sales_value' : item_dict.sales,

				}
				to_date = filters.get("to_date")
				from_date = filters.get("from_date")
				item = item_dict.item_code
				brand = item_dict.brand


				warehouses = frappe.db.sql("""select name as name from `tabWarehouse` """, as_dict=1)

				for warehouse in warehouses:
					warehousee = warehouse.name
					opening = frappe.db.sql("""select
								qty_after_transaction as res,
								valuation_rate as frate,
								stock_value as sv
								from `tabStock Ledger Entry` join `tabWarehouse` on `tabStock Ledger Entry`.warehouse = `tabWarehouse`.name
								where
								`tabStock Ledger Entry`.item_code = %s
								and `tabStock Ledger Entry`.warehouse = %s
								and `tabStock Ledger Entry`.posting_date <= %s
								and `tabStock Ledger Entry`.is_cancelled = 0
								ORDER BY `tabStock Ledger Entry`.posting_date DESC, `tabStock Ledger Entry`.posting_time DESC , `tabStock Ledger Entry`.creation DESC LIMIT 1""",
											(item, warehousee, from_date), as_dict=1)
					for tqty in opening:
						s += tqty.frate
						frat += tqty.res*tqty.frate

					# purchase_in_qty = frappe.db.sql("""select
					# 		actual_qty as qty,
					# 		valuation_rate as v_rate
					# 		from `tabStock Ledger Entry` join `tabWarehouse` on `tabStock Ledger Entry`.warehouse = `tabWarehouse`.name
					# 		where
					# 		`tabStock Ledger Entry`.item_code = %s
					# 		and (`tabStock Ledger Entry`.voucher_type = "Purchase Invoice" or `tabStock Ledger Entry`.voucher_type = "Purchase Receipt")

					# 		and `tabStock Ledger Entry`.warehouse = %s
					# 		and `tabStock Ledger Entry`.posting_date >= %s
					# 		and `tabStock Ledger Entry`.posting_date <= %s
					# 		and `tabStock Ledger Entry`.is_cancelled = 0
					# 		ORDER BY `tabStock Ledger Entry`.posting_date DESC, `tabStock Ledger Entry`.posting_time DESC , `tabStock Ledger Entry`.creation DESC """,
					# 					(item, warehousee, from_date, to_date), as_dict=1)
					# for qt in purchase_in_qty:
					# 	purchase_in_qty_value += qt.qty * qt.v_rate

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
						current_value += tqty.res * tqty.frate


					# sales_in_qty = frappe.db.sql("""select
					# 		actual_qty as qty,
					# 		valuation_rate as v_rate
					# 		from `tabStock Ledger Entry` join `tabWarehouse` on `tabStock Ledger Entry`.warehouse = `tabWarehouse`.name
					# 		where
					# 		`tabStock Ledger Entry`.item_code = %s
					# 		and (`tabStock Ledger Entry`.voucher_type = "Sales Invoice" or `tabStock Ledger Entry`.voucher_type = "Delivery Note")
					# 		and `tabStock Ledger Entry`.warehouse = %s
					# 		and `tabStock Ledger Entry`.posting_date >= %s
					# 		and `tabStock Ledger Entry`.posting_date <= %s
					# 		and `tabStock Ledger Entry`.is_cancelled = 0
					# 		ORDER BY `tabStock Ledger Entry`.posting_date DESC, `tabStock Ledger Entry`.posting_time DESC , `tabStock Ledger Entry`.creation DESC """,
					# 					(item, warehousee, from_date, to_date), as_dict=1)

					# for qt in sales_in_qty:
					# 	sales_value += qt.qty * qt.v_rate
					# frappe.throw(str(sales_value))z
			sales_value = item_dict.sales
			purchase = item_dict.purchase

			cogs = (purchase + frat) - current_value
			added_value = (sales_value) - ((purchase + frat) - current_value)
			data['opening'] = round(frat,2)
			data['total_in'] = round(purchase + frat,2)
			data['current_value'] = round(current_value,2)
			data['cogs'] = round(cogs,2)
			# data['sales_value'] = round(sales_value,2)
			data['added_value'] = round(added_value,2)
			data['cogs/sales_value'] = str(round((cogs / sales_value),2)*100)  + ' %'
			data['added_value/sales_value'] = str(round((added_value / sales_value),2) *100) + ' %'
			data['added_value/cogs'] = str(round((added_value / cogs),2)*100) + ' %'

			result.append(data)



	return result

def get_columns():
	return [
		{
			"label": _("Brand"),
			"fieldname": "brand",
			"fieldtype": "Link",
			"options": "Brand",
			"width": 150
		},
		{
			"label": _("Opening"),
			"fieldname": "opening",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"label": _("Purchase"),
			"fieldname": "purchase",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"label": _("Total In"),
			"fieldname": "total_in",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"label": _("Current Value"),
			"fieldname": "current_value",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"label": _("COGS"),
			"fieldname": "cogs",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"label": _("Sales Value"),
			"fieldname": "sales_value",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"label": _("Added Value"),
			"fieldname": "added_value",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"label": _("COGS/Sales Value"),
			"fieldname": "cogs/sales_value",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Added Value/Sales Value"),
			"fieldname": "added_value/sales_value",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Added Value/COGS"),
			"fieldname": "added_value/cogs",
			"fieldtype": "Data",
			"width": 150
		},
	]



