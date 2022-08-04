# Copyright (c) 2013, Frappe Technologies Pvt.Ltd.and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    columns = get_columns(filters)
    data = get_data(filters, columns)
    return columns, data

def get_columns(filters):
    if filters.get('tree_type') == "Sales Person":
        return [
            {
                "label": _("Sales Person"),
                "fieldname": "sales_person",
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
    if filters.get('tree_type') == "Brand":
        return [
            {
                "label": _("Brand"),
                "fieldname": "brand",
                "fieldtype": "Link",
                "options": "Brand",
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
    value_field = ""
    if filters.get("doc_type") == 'Sales Invoice' and filters.get('tree_type') == "Sales Person":
        conditions = ""
        if filters.get("value_quantity") == 'Value':
            value_field = "base_net_total"
        if filters.get("value_quantity") == 'Quantity':
            value_field = "total_qty"
        if filters.get("sales_person"):
            conditions += " and `tabSales Person`.name=%(sales_person)s"
        to_date = filters.get("to_date")
        from_date = filters.get("from_date")

        result = []
        item_results = frappe.db.sql("""
                                        SELECT 
                                        `tabSales Person`.name as sales_person,

                                        ifnull((select sum(`tabSales Invoice`.{value_field})
                                        from `tabSales Invoice` 
                                        where
                                        `tabSales Invoice`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "01"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'),0) as jan,


                                        ifnull((select sum(`tabSales Invoice`.{value_field})
                                        from `tabSales Invoice` 
                                        where
                                        `tabSales Invoice`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "02"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'),0) as feb,

                                        ifnull((select sum(`tabSales Invoice`.{value_field})
                                        from `tabSales Invoice` 
                                        where
                                        `tabSales Invoice`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "03"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'),0) as mar,

                                        ifnull((select sum(`tabSales Invoice`.{value_field})
                                        from `tabSales Invoice` 
                                        where
                                        `tabSales Invoice`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "04"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'),0) as apr,

                                        ifnull((select sum(`tabSales Invoice`.{value_field})
                                        from `tabSales Invoice` 
                                        where
                                        `tabSales Invoice`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "05"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'),0) as may,

                                        ifnull((select sum(`tabSales Invoice`.{value_field})
                                        from `tabSales Invoice` 
                                        where
                                        `tabSales Invoice`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "06"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'),0) as jun,

                                        ifnull((select sum(`tabSales Invoice`.{value_field})
                                        from `tabSales Invoice` 
                                        where
                                        `tabSales Invoice`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "07"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'),0) as jul,

                                        ifnull((select sum(`tabSales Invoice`.{value_field})
                                        from `tabSales Invoice` 
                                        where
                                        `tabSales Invoice`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "08"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'),0) as aug,

                                        ifnull((select sum(`tabSales Invoice`.{value_field})
                                        from `tabSales Invoice` 
                                        where
                                        `tabSales Invoice`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "09"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'),0) as sep,

                                        ifnull((select sum(`tabSales Invoice`.{value_field})
                                        from `tabSales Invoice` 
                                        where
                                        `tabSales Invoice`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "10"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'),0) as oct,

                                        ifnull((select sum(`tabSales Invoice`.{value_field})
                                        from `tabSales Invoice` 
                                        where
                                        `tabSales Invoice`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "11"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'),0) as nov,

                                        ifnull((select sum(`tabSales Invoice`.{value_field})
                                        from `tabSales Invoice` 
                                        where
                                        `tabSales Invoice`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "12"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'),0) as end

                                      
                                        FROM
                                            `tabSales Person`
                                        WHERE
                                            
                                            `tabSales Person`.enabled = 1
                                                {conditions}

                                       
                                        """.format(conditions=conditions, value_field=value_field,from_date=from_date,to_date=to_date), filters, as_dict=1)

        if item_results:
            for item_dict in item_results:
                data = {
                    'sales_person': item_dict.sales_person,
                    'jan': item_dict.jan,
                    'feb': item_dict.feb,
                    'apr': item_dict.apr,
                    'mar': item_dict.mar,
                    'may': item_dict.may,
                    'jun': item_dict.jun,
                    'jul': item_dict.jul,
                    'aug': item_dict.aug,
                    'sep': item_dict.sep,
                    'oct': item_dict.oct,
                    'nov': item_dict.nov,
                    'dec': item_dict.end,

                }

                result.append(data)
        return result

    if filters.get("doc_type") == 'Sales Order' and filters.get('tree_type') == "Sales Person":
        conditions = ""
        if filters.get("value_quantity") == 'Value':
            value_field = "base_net_total"
        if filters.get("value_quantity") == 'Quantity':
            value_field = "total_qty"
        if filters.get("sales_person"):
            conditions += " and `tabSales Person`.name=%(sales_person)s"
        to_date = filters.get("to_date")
        from_date = filters.get("from_date")

        result = []
        item_results = frappe.db.sql("""
                                        SELECT 
                                        `tabSales Person`.name as sales_person,

                                        ifnull((select sum(`tabSales Order`.{value_field})
                                        from `tabSales Order` 
                                        where
                                        `tabSales Order`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "01"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'),0) as jan,


                                        ifnull((select sum(`tabSales Order`.{value_field})
                                        from `tabSales Order` 
                                        where
                                        `tabSales Order`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "02"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'),0) as feb,

                                        ifnull((select sum(`tabSales Order`.{value_field})
                                        from `tabSales Order` 
                                        where
                                        `tabSales Order`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "03"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'),0) as mar,

                                        ifnull((select sum(`tabSales Order`.{value_field})
                                        from `tabSales Order` 
                                        where
                                        `tabSales Order`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "04"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'),0) as apr,

                                        ifnull((select sum(`tabSales Order`.{value_field})
                                        from `tabSales Order` 
                                        where
                                        `tabSales Order`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "05"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'),0) as may,

                                        ifnull((select sum(`tabSales Order`.{value_field})
                                        from `tabSales Order` 
                                        where
                                        `tabSales Order`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "06"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'),0) as jun,

                                        ifnull((select sum(`tabSales Order`.{value_field})
                                        from `tabSales Order` 
                                        where
                                        `tabSales Order`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "07"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'),0) as jul,

                                        ifnull((select sum(`tabSales Order`.{value_field})
                                        from `tabSales Order` 
                                        where
                                        `tabSales Order`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "08"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'),0) as aug,

                                        ifnull((select sum(`tabSales Order`.{value_field})
                                        from `tabSales Order` 
                                        where
                                        `tabSales Order`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "09"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'),0) as sep,

                                        ifnull((select sum(`tabSales Order`.{value_field})
                                        from `tabSales Order` 
                                        where
                                        `tabSales Order`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "10"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'),0) as oct,

                                        ifnull((select sum(`tabSales Order`.{value_field})
                                        from `tabSales Order` 
                                        where
                                        `tabSales Order`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "11"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'),0) as nov,

                                        ifnull((select sum(`tabSales Order`.{value_field})
                                        from `tabSales Order` 
                                        where
                                        `tabSales Order`.sales_person =`tabSales Person`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "12"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'),0) as end

                                      
                                        FROM
                                            `tabSales Person`
                                        WHERE
                                            
                                            `tabSales Person`.enabled = 1
                                                {conditions}

                                       
                                        """.format(conditions=conditions, value_field=value_field,from_date=from_date,to_date=to_date), filters, as_dict=1)

        if item_results:
            for item_dict in item_results:
                data = {
                    'sales_person': item_dict.sales_person,
                    'jan': item_dict.jan,
                    'feb': item_dict.feb,
                    'apr': item_dict.apr,
                    'mar': item_dict.mar,
                    'may': item_dict.may,
                    'jun': item_dict.jun,
                    'jul': item_dict.jul,
                    'aug': item_dict.aug,
                    'sep': item_dict.sep,
                    'oct': item_dict.oct,
                    'nov': item_dict.nov,
                    'dec': item_dict.end,

                }

                result.append(data)
        return result

    if filters.get("doc_type") == 'Sales Invoice' and filters.get('tree_type') == "Brand":
        conditions = ""
        if filters.get("value_quantity") == 'Value':
            value_field = "base_net_amount"
        if filters.get("value_quantity") == 'Quantity':
            value_field = "qty"
        if filters.get("sales_person"):
            conditions += " and `tabSales Invoice`.sales_person=%(sales_person)s"
        to_date = filters.get("to_date")
        from_date = filters.get("from_date")

        result = []
        item_results = frappe.db.sql("""
                                        SELECT 
                                        `tabBrand`.name as brand,

                                        ifnull((select sum(`tabSales Invoice Item`.{value_field})
                                        from `tabSales Invoice Item` join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
                                        where
										`tabSales Invoice Item`.brand = `tabBrand`.name 
										and MONTH(`tabSales Invoice`.posting_date) = "01"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'  {conditions}),0) as jan,


                                      
                                        ifnull((select sum(`tabSales Invoice Item`.{value_field})
                                        from `tabSales Invoice Item` join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
                                        where
										`tabSales Invoice Item`.brand = `tabBrand`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "02"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'  {conditions}),0) as feb,

                                        
                                        ifnull((select sum(`tabSales Invoice Item`.{value_field})
                                        from `tabSales Invoice Item` join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
                                        where
										`tabSales Invoice Item`.brand = `tabBrand`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "03"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'  {conditions}),0) as mar,

                                        
                                        ifnull((select sum(`tabSales Invoice Item`.{value_field})
                                        from `tabSales Invoice Item` join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
                                        where
										`tabSales Invoice Item`.brand = `tabBrand`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "04"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'  {conditions}),0) as apr,

                                       
                                        ifnull((select sum(`tabSales Invoice Item`.{value_field})
                                        from `tabSales Invoice Item` join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
                                        where
										`tabSales Invoice Item`.brand = `tabBrand`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "05"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'  {conditions}),0) as may,

                                       
                                        ifnull((select sum(`tabSales Invoice Item`.{value_field})
                                        from `tabSales Invoice Item` join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
                                        where
										`tabSales Invoice Item`.brand = `tabBrand`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "06"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'  {conditions}),0) as jun,

                                       
                                        ifnull((select sum(`tabSales Invoice Item`.{value_field})
                                        from `tabSales Invoice Item` join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
                                        where
										`tabSales Invoice Item`.brand = `tabBrand`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "07"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'  {conditions}),0) as jul,

                                       
                                        ifnull((select sum(`tabSales Invoice Item`.{value_field})
                                        from `tabSales Invoice Item` join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
                                        where
										`tabSales Invoice Item`.brand = `tabBrand`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "08"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'  {conditions}),0) as aug,

                                       
                                        ifnull((select sum(`tabSales Invoice Item`.{value_field})
                                        from `tabSales Invoice Item` join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
                                        where
										`tabSales Invoice Item`.brand = `tabBrand`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "09"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'  {conditions}),0) as sep,

                                       
                                        ifnull((select sum(`tabSales Invoice Item`.{value_field})
                                        from `tabSales Invoice Item` join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
                                        where
										`tabSales Invoice Item`.brand = `tabBrand`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "10"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'  {conditions}),0) as oct,

                                        
                                        ifnull((select sum(`tabSales Invoice Item`.{value_field})
                                        from `tabSales Invoice Item` join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
                                        where
										`tabSales Invoice Item`.brand = `tabBrand`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "11"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'  {conditions}),0) as nov,

                                       
                                        ifnull((select sum(`tabSales Invoice Item`.{value_field})
                                        from `tabSales Invoice Item` join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent 
                                        where
										`tabSales Invoice Item`.brand = `tabBrand`.name
                                        and MONTH(`tabSales Invoice`.posting_date) = "12"
                                        and `tabSales Invoice`.docstatus = 1
                                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'  {conditions}),0) as end

                                      
                                        FROM
                                            `tabBrand`
                                       
                                            
                                               

                                       
                                        """.format(conditions=conditions, value_field=value_field,from_date=from_date,to_date=to_date), filters, as_dict=1)

        if item_results:
            for item_dict in item_results:
                data = {
                    'brand': item_dict.brand,
                    'jan': item_dict.jan,
                    'feb': item_dict.feb,
                    'apr': item_dict.apr,
                    'mar': item_dict.mar,
                    'may': item_dict.may,
                    'jun': item_dict.jun,
                    'jul': item_dict.jul,
                    'aug': item_dict.aug,
                    'sep': item_dict.sep,
                    'oct': item_dict.oct,
                    'nov': item_dict.nov,
                    'dec': item_dict.end,

                }

                result.append(data)
        return result


    if filters.get("doc_type") == 'Sales Order' and filters.get('tree_type') == "Brand":
        conditions = ""
        if filters.get("value_quantity") == 'Value':
            value_field = "base_net_amount"
        if filters.get("value_quantity") == 'Quantity':
            value_field = "qty"
        if filters.get("sales_person"):
            conditions += " and `tabSales Order`.sales_person=%(sales_person)s"
        to_date = filters.get("to_date")
        from_date = filters.get("from_date")

        result = []
        item_results = frappe.db.sql("""
                                        SELECT 
                                        `tabBrand`.name as brand,

                                        ifnull((select sum(`tabSales Order Item`.{value_field})
                                        from `tabSales Order Item` join `tabSales Order` on `tabSales Order`.name = `tabSales Order Item`.parent 
                                        where
										`tabSales Order Item`.brand = `tabBrand`.name 
										and MONTH(`tabSales Order`.transaction_date) = "01"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'  {conditions}),0) as jan,


                                      
                                        ifnull((select sum(`tabSales Order Item`.{value_field})
                                        from `tabSales Order Item` join `tabSales Order` on `tabSales Order`.name = `tabSales Order Item`.parent 
                                        where
										`tabSales Order Item`.brand = `tabBrand`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "02"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'  {conditions}),0) as feb,

                                        
                                        ifnull((select sum(`tabSales Order Item`.{value_field})
                                        from `tabSales Order Item` join `tabSales Order` on `tabSales Order`.name = `tabSales Order Item`.parent 
                                        where
										`tabSales Order Item`.brand = `tabBrand`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "03"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'  {conditions}),0) as mar,

                                        
                                        ifnull((select sum(`tabSales Order Item`.{value_field})
                                        from `tabSales Order Item` join `tabSales Order` on `tabSales Order`.name = `tabSales Order Item`.parent 
                                        where
										`tabSales Order Item`.brand = `tabBrand`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "04"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'  {conditions}),0) as apr,

                                       
                                        ifnull((select sum(`tabSales Order Item`.{value_field})
                                        from `tabSales Order Item` join `tabSales Order` on `tabSales Order`.name = `tabSales Order Item`.parent 
                                        where
										`tabSales Order Item`.brand = `tabBrand`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "05"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'  {conditions}),0) as may,

                                       
                                        ifnull((select sum(`tabSales Order Item`.{value_field})
                                        from `tabSales Order Item` join `tabSales Order` on `tabSales Order`.name = `tabSales Order Item`.parent 
                                        where
										`tabSales Order Item`.brand = `tabBrand`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "06"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'  {conditions}),0) as jun,

                                       
                                        ifnull((select sum(`tabSales Order Item`.{value_field})
                                        from `tabSales Order Item` join `tabSales Order` on `tabSales Order`.name = `tabSales Order Item`.parent 
                                        where
										`tabSales Order Item`.brand = `tabBrand`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "07"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'  {conditions}),0) as jul,

                                       
                                        ifnull((select sum(`tabSales Order Item`.{value_field})
                                        from `tabSales Order Item` join `tabSales Order` on `tabSales Order`.name = `tabSales Order Item`.parent 
                                        where
										`tabSales Order Item`.brand = `tabBrand`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "08"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'  {conditions}),0) as aug,

                                       
                                        ifnull((select sum(`tabSales Order Item`.{value_field})
                                        from `tabSales Order Item` join `tabSales Order` on `tabSales Order`.name = `tabSales Order Item`.parent 
                                        where
										`tabSales Order Item`.brand = `tabBrand`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "09"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'  {conditions}),0) as sep,

                                       
                                        ifnull((select sum(`tabSales Order Item`.{value_field})
                                        from `tabSales Order Item` join `tabSales Order` on `tabSales Order`.name = `tabSales Order Item`.parent 
                                        where
										`tabSales Order Item`.brand = `tabBrand`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "10"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'  {conditions}),0) as oct,

                                        
                                        ifnull((select sum(`tabSales Order Item`.{value_field})
                                        from `tabSales Order Item` join `tabSales Order` on `tabSales Order`.name = `tabSales Order Item`.parent 
                                        where
										`tabSales Order Item`.brand = `tabBrand`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "11"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'  {conditions}),0) as nov,

                                       
                                        ifnull((select sum(`tabSales Order Item`.{value_field})
                                        from `tabSales Order Item` join `tabSales Order` on `tabSales Order`.name = `tabSales Order Item`.parent 
                                        where
										`tabSales Order Item`.brand = `tabBrand`.name
                                        and MONTH(`tabSales Order`.transaction_date) = "12"
                                        and `tabSales Order`.docstatus = 1
                                        and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'  {conditions}),0) as end

                                      
                                        FROM
                                            `tabBrand`
                                       
                                            
                                               

                                       
                                        """.format(conditions=conditions, value_field=value_field,from_date=from_date,to_date=to_date), filters, as_dict=1)

        if item_results:
            for item_dict in item_results:
                data = {
                    'brand': item_dict.brand,
                    'jan': item_dict.jan,
                    'feb': item_dict.feb,
                    'apr': item_dict.apr,
                    'mar': item_dict.mar,
                    'may': item_dict.may,
                    'jun': item_dict.jun,
                    'jul': item_dict.jul,
                    'aug': item_dict.aug,
                    'sep': item_dict.sep,
                    'oct': item_dict.oct,
                    'nov': item_dict.nov,
                    'dec': item_dict.end,

                }

                result.append(data)
        return result














