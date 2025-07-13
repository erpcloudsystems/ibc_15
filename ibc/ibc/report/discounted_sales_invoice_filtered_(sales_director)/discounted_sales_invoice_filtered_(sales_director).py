

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
            "label": _("Sales Invoice"),
            "fieldname": "sales_invoice",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 180
        },
        {
            "label": _("Status"),
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 95
        },
        {
            "label": _("Sales Person"),
            "fieldname": "sales_person",
            "fieldtype": "Link",
            "options": "Sales Person",
            "width": 145
        },
        {
            "label": _("Customer"),
            "fieldname": "customer",
            "fieldtype": "Data",
            "width": 195
        },
        {
            "label": _("Item Code"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 90
        },
        {
            "label": _("Item Name"),
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 155
        },
        {
            "label": _("Item Group"),
            "fieldname": "item_group",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Brand"),
            "fieldname": "brand",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Qty"),
            "fieldname": "qty",
            "fieldtype": "Float",
            "width": 60
        },
        {
            "label": _("Disc (%)"),
            "fieldname": "discount_percentage",
            "fieldtype": "Percent",
            "width": 80
        },
        {
            "label": _("Price List"),
            "fieldname": "price_list_rate",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": _("Price"),
            "fieldname": "rate",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": _("Net Amount"),
            "fieldname": "net_amount",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": _("Amount"),
            "fieldname": "amount",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": _("Return"),
            "fieldname": "is_return",
            "fieldtype": "Check",
            "width": 70
        }
    ]

def get_data(filters, columns):
    item_price_qty_data = get_item_price_qty_data(filters)
    # totals = calculate_totals(item_price_qty_data)
    # item_price_qty_data.append(totals)
    return item_price_qty_data

def get_item_price_qty_data(filters):
    conditions = []
    conditions.append("1 = 1")

    if filters.get("from_date"):
        conditions.append("`tabSales Invoice`.posting_date>=%(from_date)s")
    if filters.get("to_date"):
        conditions.append("`tabSales Invoice`.posting_date<=%(to_date)s")
    if filters.get("brand"):
        conditions.append("`tabSales Invoice Item`.brand=%(brand)s")
    if filters.get("sales_person"):
        conditions.append("`tabSales Invoice`.sales_person = %(sales_person)s")
    if filters.get("show_only_maintain_stock"):
        conditions.append("`tabSales Invoice Item`.is_stock_item = 1")

    conditions = " and ".join(conditions)

    item_results = frappe.db.sql(""" select
                                        `tabSales Invoice`.name as sales_invoice,
                                        `tabSales Invoice`.posting_date as posting_date,
                                        `tabSales Invoice`.sales_person as sales_person,
                                        `tabSales Invoice`.customer as customer,
                                        `tabSales Invoice Item`.item_code as item_code,
                                        `tabSales Invoice Item`.item_name as item_name,
                                        `tabSales Invoice Item`.qty as qty,
                                        `tabSales Invoice Item`.discount_percentage as discount_percentage,
                                        `tabSales Invoice Item`.price_list_rate as price_list_rate,
                                        `tabSales Invoice Item`.rate as rate,
                                        `tabSales Invoice Item`.item_group as item_group,
                                        `tabSales Invoice Item`.brand as brand,
                                        `tabSales Invoice`.status as status,
                                        `tabSales Invoice Item`.net_amount as net_amount,
                                        `tabSales Invoice Item`.amount as amount,
                                        `tabSales Invoice`.is_return as is_return
                                    from
                                        `tabSales Invoice`
                                        join `tabSales Invoice Item` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent
                                        join `tabSales Person` on `tabSales Person`.name = `tabSales Invoice`.sales_person
                                    where
                                        `tabSales Invoice`.docstatus = 1
                                    and `tabSales Person`.parent_sales_person in ('Sales Director','6th October','Alexandria','Head Office','Demo','Hurgada','Down Town')
                                    and {conditions}
                                """
        .format(conditions=conditions), filters, as_dict=1)


    result = []
    if item_results:
        for item_dict in item_results:
            data = {
                'sales_invoice': item_dict.sales_invoice,
                'posting_date': item_dict.posting_date,
                'sales_person': item_dict.sales_person,
                'customer': item_dict.customer,
                'item_code': item_dict.item_code,
                'item_name': item_dict.item_name,
                'qty': item_dict.qty,
                'discount_percentage': item_dict.discount_percentage,
                'price_list_rate': item_dict.price_list_rate,
                'rate': item_dict.rate,
                'item_group': item_dict.item_group,
                'brand': item_dict.brand,
                'status': item_dict.status,
                'net_amount': item_dict.net_amount,
                'amount': item_dict.amount,
                'is_return': item_dict.is_return
            }
            result.append(data)

    return result

def calculate_totals(data):
    total_qty = 0
    total_net_amount = 0
    total_amount = 0

    for item in data:
        if item.get('sales_person') != 'Demo':
            total_qty += item.get('qty', 0)
            total_net_amount += item.get('net_amount', 0)
            total_amount += item.get('amount', 0)

    return {
        'sales_invoice': 'Total',
        'qty': total_qty,
        'net_amount': total_net_amount,
        'amount': total_amount
    }