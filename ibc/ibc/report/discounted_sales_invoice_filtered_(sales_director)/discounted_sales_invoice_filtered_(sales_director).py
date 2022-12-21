from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {
            'fieldname': 'posting_date',
            'fieldtype': 'Link',
            'label': _('Date'),
            'options': 'Sales Invoice'
        },
        {
            'fieldname': 'name',
            'fieldtype': 'Link',
            'label': _('Sales Invoice'),
            'options': 'Sales Invoice'
        },
        {
            'fieldname': 'customer_name',
            'fieldtype': 'Link',
            'label': _('Customer'),
            'options': 'Sales Invoice'
        },
        {
            'fieldname': 'grand_total',
            'fieldtype': 'Float',
            'label': _('Grand Total'),
        },
        {
            'fieldname': 'total_discount',
            'fieldtype': 'Float',
            'label': _('Item Discount'),
        },
        {
            'fieldname': 'discount_amount',
            'fieldtype': 'Float',
            'label': _('Additional Discount'),
        },
        {
            'fieldname': 'net_total',
            'fieldtype': 'Float',
            'label': _('Net Total'),
        },
        {
            'fieldname': 'payment',
            'fieldtype': 'Link',
            'label': _('Mode Of Payment'),
            'options': 'Sales Invoice'
        },
        {
            'fieldname': 'source',
            'fieldtype': 'Link',
            'label': _('Source'),
            'options': 'Sales Invoice'
        },
        {
            'fieldname': 'mobile_no',
            'fieldtype': 'Link',
            'label': _('Mobile Number'),
            'options': 'Customer'
        },
        {
            'fieldname': 't_sales_person',
            'fieldtype': 'Link',
            'label': _('T Sales Person'),
            'options': 'Sales Invoice'
        },
        {
            'fieldname': 'o_sales_person',
            'fieldtype': 'Link',
            'label': _('O Sales Person'),
            'options': 'Customer'
        },
    ]




def get_data(filters):
    conditions = ""
    salesp=filters.get("sales_person")
    if filters.get("sales_person"):
        conditions += f" and `tabSales Invoice`.sales_person = '{salesp}'"

    if filters.get("to_date"):
        conditions += " AND `tabSales Invoice`.posting_date <='%s'" % filters.get("to_date")
    if filters.get("from_date"):
        conditions += " AND `tabSales Invoice`.posting_date >='%s'" % filters.get("from_date")

    data = frappe.db.sql(f"""
    select
    `tabSales Invoice`.posting_date as posting_date,
    `tabSales Invoice`.name as name,
    `tabSales Invoice`.customer_name as customer_name,
    ((select sum(`tabSales Invoice Item`.amount) from `tabSales Invoice Item` where `tabSales Invoice Item`.parent = `tabSales Invoice`.name and `tabSales Invoice Item`.item_group not in ('2-Service','ID Printed','Maintenance contracts','Services1')) + (select sum(`tabSales Invoice Item`.item_discount) from `tabSales Invoice Item` where `tabSales Invoice Item`.parent = `tabSales Invoice`.name and `tabSales Invoice Item`.item_group not in ('2-Service','ID Printed','Maintenance contracts','Services1'))) as grand_total,
    (select sum(`tabSales Invoice Item`.item_discount) from `tabSales Invoice Item` where `tabSales Invoice Item`.parent = `tabSales Invoice`.name and `tabSales Invoice Item`.item_group not in ('2-Service','ID Printed','Maintenance contracts','Services1')) as total_discount,
    `tabSales Invoice`.discount_amount as discount_amount,
    ((select sum(`tabSales Invoice Item`.amount) from `tabSales Invoice Item` where `tabSales Invoice Item`.parent = `tabSales Invoice`.name and `tabSales Invoice Item`.item_group not in ('2-Service','ID Printed','Maintenance contracts','Services1')) - `tabSales Invoice`.discount_amount) as net_total,
    `tabSales Invoice`.payment as payment,
    `tabSales Invoice`.source as source,
    `tabCustomer`.mobile_no as mobile_no,
    `tabSales Invoice`.sales_person as t_sales_person,
    `tabCustomer`.sales_person as o_sales_person

    from `tabSales Invoice`
     join `tabCustomer`
         on `tabSales Invoice`.customer = `tabCustomer`.name
     join `tabSales Person`
         on `tabSales Invoice`.sales_person = `tabSales Person`.name
    where
    `tabSales Invoice`.docstatus =1
    and `tabSales Person`.parent_sales_person in ('6th October','Alexandria','Down Town','Head Office','Hurgada','New Cairo')
    {conditions}
    """,as_dict=True)


    return data

