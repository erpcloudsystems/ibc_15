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
            "label": _("Ticket"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Ticket",
            "width": 130
        },
        {
            "label": _("Date"),
            "fieldname": _("posting_date"),
            "fieldtype": "date",
            "width": 100
        },
        {
            "label": _("Status"),
            "fieldname": "workflow_state",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": _("Approval Date"),
            "fieldname": _("approval_date"),
            "fieldtype": "date",
            "width": 100
        },
        {
            "label": _("Item Code"),
            "fieldname": "item_code",
            "options": "Item",
            "fieldtype": "Link",
            "width": 100
        },
        {
            "label": _("Item Name"),
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 200
        },
		{
			"label": _("Item Group"),
			"fieldname": "item_group",
			"fieldtype": "Data",
			"width": 100
		},
        {
            "label": _("Debit"),
            "fieldname": "cost",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": _("حسابات"),
            "fieldname": "new_accounts",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": _("داخلى"),
            "fieldname": "new_internal",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": _("صافى"),
            "fieldname": "new_clear",
            "fieldtype": "Currency",
            "width": 100
        },

        {
            "label": _("Customer Name"),
            "fieldname": "customer_name",
            "fieldtype": "Data",
            "width": 200
        },

        {
            "label": _("Maintenanc Customer Name"),
            "fieldname": "maintenanc_customer_name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Spare Parts"),
            "fieldname": "spare_parts",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Installation Engineer"),
            "fieldname": _("full_name"),
            "fieldtype": "Data",
            "width": 150
        }
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " and `tabTicket`.posting_date>=%(from_date)s"
    if filters.get("to_date"):
        conditions += " and `tabTicket`.posting_date<=%(to_date)s"
    if filters.get("installation_engineer"):
        conditions += " and `tabTicket`.installation_engineer =%(installation_engineer)s"
    item_results = frappe.db.sql("""
                select
                        `tabTicket`.name as name,
                        `tabTicket`.workflow_state as workflow_state,
                        `tabTicket`.posting_date as posting_date,
                        `tabTicket Items`.item_code as item_code,
                        `tabTicket Items`.item_name as item_name,
                        `tabTicket Items`.cost as cost,
                        `tabTicket Items`.new_accounts as new_accounts,
                        `tabTicket Items`.item_group as item_group,
                        `tabTicket Items`.new_internal as new_internal,
                        `tabTicket Items`.new_clear as new_clear,
                        `tabTicket`.customer_name as customer_name,
                        `tabTicket`.maintenanc_customer_name as maintenanc_customer_name,
                        `tabTicket Items`.spare_parts as spare_parts,
                        `tabTicket`.installation_engineer as installation_engineer
                from
                        `tabTicket` join `tabTicket Items` on `tabTicket`.name = `tabTicket Items`.parent
                where
                        `tabTicket`.docstatus != 2
                {conditions}
                """.format(conditions=conditions), filters, as_dict=1)

    # price_list_names = list(set([item.price_list_name for item in item_results]))

    # buying_price_map = get_price_map(price_list_names, buying=1)
    # selling_price_map = get_price_map(price_list_names, selling=1)

    result = []
    if item_results:
        for item_dict in item_results:
            approval_date = frappe.db.get_value('Comment', {'reference_name': item_dict.name, 'content': "Approved"}, ['creation'])
            full_name = frappe.db.get_value('User',item_dict.installation_engineer,'full_name')
            data = {
                'name': item_dict.name,
                'posting_date': item_dict.posting_date,
                'workflow_state': item_dict.workflow_state,
                'approval_date': approval_date,
                'item_code': item_dict.item_code,
                'item_name': item_dict.item_name,
                'cost': item_dict.cost,
                'new_accounts': item_dict.new_accounts,
                'item_group': item_dict.item_group,
                'new_internal': item_dict.new_internal,
                'new_clear': _(item_dict.new_clear),
                'customer_name': _(item_dict.customer_name),
                'maintenanc_customer_name': item_dict.maintenanc_customer_name,
                'spare_parts':item_dict.spare_parts,
                'full_name': full_name,

            }
            result.append(data)

    return result
