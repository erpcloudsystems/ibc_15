# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns=get_columns(filters)
	data=get_data(filters,columns)
	return columns, data

def get_columns(filters):
	if filters.get('tree_type') == "Sales Person":
		return [
			{
				"label": _("Sales Person"),
				"fieldname": "sales_persone",
				"fieldtype": "Link",
				"options": "Sales Person",
				"width": 150
			},
			{
				"label": _("Jan"),
				"fieldname": "jan",
				"fieldtype": "Currency",
				"width": 150
			},
			{
				"label": _("Feb"),
				"fieldname": "feb",
				"fieldtype": "Currency",
				"width": 150
			},
			{
				"label": _("Mar"),
				"fieldname": "mar",
				"fieldtype": "Currency",
				"width": 150
			},
			{
				"label": _("Apr"),
				"fieldname": "apr",
				"fieldtype": "Currency",
				"width": 150
			},
			{
				"label": _("May"),
				"fieldname": "may",
				"fieldtype": "Currency",
				"width": 150
			},
			{
				"label": _("Jun"),
				"fieldname": "jun",
				"fieldtype": "Currency",
				"width": 150
			},
			{
				"label": _("Jul"),
				"fieldname": "jul",
				"fieldtype": "Currency",
				"width": 150
			},
			{
				"label": _("Aug"),
				"fieldname": "aug",
				"fieldtype": "Currency",
				"width": 150
			},
			{
				"label": _("Sep"),
				"fieldname": "sep",
				"fieldtype": "Currency",
				"width": 150
			},
			{
				"label": _("Oct"),
				"fieldname": "oct",
				"fieldtype": "Currency",
				"width": 150
			},
			{
				"label": _("Nov"),
				"fieldname": "nov",
				"fieldtype": "Currency",
				"width": 150
			},
			{
				"label": _("Dec"),
				"fieldname": "dec",
				"fieldtype": "Currency",
				"width": 150
			}
		]
def get_data(filters, columns):
	item_price_qty_data = []
	item_price_qty_data = get_item_price_qty_data(filters)
	return item_price_qty_data

def get_item_price_qty_data(filters):
	conditions = ""
	if filters.get("doc_type") == 'Sales Order':
		date_field = 'transaction_date'
	if filters.get("doc_type") == 'Sales Invoice':
		date_field = 'posting_date'
	conditions = ""
	if filters.get("value_quantity") == 'Value':
		value_field = " total"
	if filters.get("value_quantity") == 'Value':
		value_field = "total_qty"
	if filters.get("doc_type") == 'Sales Order':
		doctype = "Sales Order"
	if filters.get("doc_type") == 'Sales Invoice':
		doctype = "Sales Invoice"
	if filters.get("from_date"):
		conditions += " and `tabSales Invoice`.posting_date>=%(from_date)s"
	if filters.get("to_date"):
		conditions += " and `tabSales Invoice`.posting_date<=%(to_date)s"
	if filters.get("sales_person"):
		conditions += " and `tabSales Invoice`.sales_person=%(sales_person)s"
	
	# Start getting all qty
	s1 = 0
	s2 = 0
	s3 = 0
	s4 = 0
	s5 = 0
	s6 = 0
	s7 = 0
	s8 = 0
	s9 = 0
	s10 = 0
	s11 = 0
	s12 = 0

	# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
	jan = frappe.db.sql("""select
									ifnull(sum( total),0) as res,
									`tabSales Invoice`.sales_person as sales_persone
									from `tabSales Invoice` 
									where
									MONTH(`tabSales Invoice`.posting_date) = "01"
									and `tabSales Invoice`.docstatus = 1
										{conditions}
										
									""".format( value_field=value_field, doctype=doctype, conditions=conditions, date_field=date_field ),filters, as_dict=1)
	for tqty in jan:
		s1 += tqty.res
		sales_persone = tqty.sales_persone
	

	# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
	feb = frappe.db.sql("""select
									ifnull(sum( total),0) as res,
									`tabSales Invoice`.sales_person as sales_persone
									from `tabSales Invoice` 
									where
									MONTH(`tabSales Invoice`.posting_date) = "02"
									and `tabSales Invoice`.docstatus = 1
										{conditions}
										
									""".format( value_field=value_field, doctype=doctype, conditions=conditions, date_field=date_field ),filters, as_dict=1)
	for tqty in feb:
		s2 += tqty.res
		sales_persone = tqty.sales_persone
	

	# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
	mar = frappe.db.sql("""select
									ifnull(sum( total),0) as res,
									`tabSales Invoice`.sales_person as sales_persone
									from `tabSales Invoice` 
									where
									MONTH(`tabSales Invoice`.posting_date) = "03"
									and `tabSales Invoice`.docstatus = 1
										{conditions}
										
									""".format( value_field=value_field, doctype=doctype, conditions=conditions, date_field=date_field ),filters, as_dict=1)
	for tqty in mar:
		s3 += tqty.res
		sales_persone = tqty.sales_persone
	

	# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
	apr = frappe.db.sql("""select
									ifnull(sum( total),0) as res,
									`tabSales Invoice`.sales_person as sales_persone
									from `tabSales Invoice` 
									where
									MONTH(`tabSales Invoice`.posting_date) = "04"
									and `tabSales Invoice`.docstatus = 1
										{conditions}
										
									""".format( value_field=value_field, doctype=doctype, conditions=conditions, date_field=date_field ),filters, as_dict=1)
	for tqty in apr:
		s4 += tqty.res
		sales_persone = tqty.sales_persone
	

	# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
	may = frappe.db.sql("""select
									ifnull(sum( total),0) as res,
									`tabSales Invoice`.sales_person as sales_persone
									from `tabSales Invoice` 
									where
									MONTH(`tabSales Invoice`.posting_date) = "05"
									and `tabSales Invoice`.docstatus = 1
										{conditions}
										
									""".format( value_field=value_field, doctype=doctype, conditions=conditions, date_field=date_field ), filters, as_dict=1)
	for tqty in may:
		s5 += tqty.res
		sales_persone = tqty.sales_persone
	

	# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
	jun = frappe.db.sql("""select
									ifnull(sum( total),0) as res,
									`tabSales Invoice`.sales_person as sales_persone
									from `tabSales Invoice` 
									where
									MONTH(`tabSales Invoice`.posting_date) = "06"
									and `tabSales Invoice`.docstatus = 1
										{conditions}
										
									""".format( value_field=value_field, doctype=doctype, conditions=conditions, date_field=date_field ),filters, as_dict=1)
	for tqty in jun:
		s6 += tqty.res
		sales_persone = tqty.sales_persone
	

	# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
	jul = frappe.db.sql("""select
									ifnull(sum( total),0) as res,
									`tabSales Invoice`.sales_person as sales_persone
									from `tabSales Invoice` 
									where
									MONTH(`tabSales Invoice`.posting_date) = "07"
									and `tabSales Invoice`.docstatus = 1
										{conditions}
										
									""".format( value_field=value_field, doctype=doctype, conditions=conditions, date_field=date_field ), filters, as_dict=1)
	for tqty in jul:
		s7 += tqty.res
		sales_persone = tqty.sales_persone
	

	# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
	aug = frappe.db.sql("""select
									ifnull(sum( total),0) as res,
									`tabSales Invoice`.sales_person as sales_persone
									from `tabSales Invoice` 
									where
									MONTH(`tabSales Invoice`.posting_date) = "08"
									and `tabSales Invoice`.docstatus = 1
										{conditions}
										
									""".format( value_field=value_field, doctype=doctype, conditions=conditions, date_field=date_field ), filters, as_dict=1)
	for tqty in aug:
		s8 += tqty.res
		sales_persone = tqty.sales_persone
	

	# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
	sep = frappe.db.sql("""select
									ifnull(sum( total),0) as res,
									`tabSales Invoice`.sales_person as sales_persone
									from `tabSales Invoice` 
									where
									MONTH(`tabSales Invoice`.posting_date) = "09"
									and `tabSales Invoice`.docstatus = 1
										{conditions}
										
									""".format( value_field=value_field, doctype=doctype, conditions=conditions, date_field=date_field ),filters, as_dict=1)
	for tqty in sep:
		s9 += tqty.res
		sales_persone = tqty.sales_persone


	# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
	oct = frappe.db.sql("""select
									ifnull(sum( total),0) as res,
									`tabSales Invoice`.sales_person as sales_persone
									from `tabSales Invoice` 
									where
									MONTH(`tabSales Invoice`.posting_date) = "10"
									and `tabSales Invoice`.docstatus = 1
										{conditions}
										
									""".format( value_field=value_field, doctype=doctype, conditions=conditions, date_field=date_field ),filters, as_dict=1)
	for tqty in oct:
		s10 += tqty.res
		sales_persone = tqty.sales_persone
	

	# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
	nov = frappe.db.sql("""select
									ifnull(sum( total),0) as res,
									`tabSales Invoice`.sales_person as sales_persone
									from `tabSales Invoice` 
									where
									MONTH(`tabSales Invoice`.posting_date) = "11"
									and `tabSales Invoice`.docstatus = 1
										{conditions}
										
									""".format( value_field=value_field, doctype=doctype, conditions=conditions, date_field=date_field ),filters, as_dict=1)
	for tqty in nov:
		s11 += tqty.res
		sales_persone = tqty.sales_persone
	

	# ///////////////////////////////////////////////////////////////////////////////////////////////////////////
	dec = frappe.db.sql("""select
									ifnull(sum( total),0) as res,
									`tabSales Invoice`.sales_person as sales_persone
									from `tabSales Invoice` 
									where
									MONTH(`tabSales Invoice`.posting_date) = "12"
									and `tabSales Invoice`.docstatus = 1
										{conditions}
										
									""".format( value_field=value_field, doctype=doctype, conditions=conditions, date_field=date_field ), filters, as_dict=1)
	for tqty in dec:
		s12 += tqty.res
		sales_persone = tqty.sales_persone


				# ///////////////////////////////////////////////////////////////////////////////////////////////////////////

	result = []
	
	data = {
		
		'jan': s1,
		'feb': s2,
		'mar': s3,
		'apr': s4,
		'may': s5,
		'jun': s6,
		'jul': s7,
		'aug': s8,
		'sep': s9,
		'oct': s10,
		'nov': s11,
		'dec': s12,
		'sales_persone': sales_persone,
	}
	result.append(data)

	return result