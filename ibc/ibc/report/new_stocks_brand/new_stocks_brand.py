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
            "width": 150,
        },
        {
            "label": _("Item Name"),
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("Brand"),
            "fieldname": "brand",
            "fieldtype": "Link",
            "options": "Brand",
            "width": 150,
        },
        {
            "label": _("Warehouse"),
            "fieldname": "warehouse",
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 150,
        },
        {
            "label": _("Total Value"),
            "fieldname": "total_value",
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "label": _("Valuation Rate"),
            "fieldname": "valuation_rate",
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "label": _("Total Qty"),
            "fieldname": "total_qty",
            "fieldtype": "Float",
            "width": 150,
        },
        {
            "label": _("Summary QTY"),
            "fieldname": "summary_qty",
            "fieldtype": "Float",
            "width": 150,
        },
        {
            "label": _("Not Summary QTY"),
            "fieldname": "not_summary_qty",
            "fieldtype": "Float",
            "width": 150,
        },
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    if filters.get("brand"):
        conditions += " and `tabItem`.brand=%(brand)s"
    item_results = frappe.db.sql(
        """
                SELECT distinct
                    ifnull(`tabItem`.name,0) as item_code,
                    ifnull(`tabItem`.item_name,0) as item_name,
                    ifnull(`tabItem`.brand,0) as brand,
                    ifnull(`tabBin`.valuation_rate,0) as valuation_rate
                from
                    `tabItem` left join `tabBin` on `tabItem`.name = `tabBin`.item_code
                where
                `tabItem`.disabled in (0, 1)
                and `tabBin`.warehouse = "المخزن الرئيسي - IBC"
                    {conditions}
                """.format(
            conditions=conditions
        ),
        filters,
        as_dict=1,
    )

    result = []
    if item_results:
        for item_dict in item_results:

            data = {
                "item_code": item_dict.item_code,
                "brand": (item_dict.brand),
                "item_name": (item_dict.item_name),
                "valuation_rate": item_dict.valuation_rate,
            }
            from_date = filters.get("from_date")
            item = item_dict.item_code

            warehouses = frappe.db.sql(
                """select name as name from `tabWarehouse` where disabled = 0""",
                as_dict=1,
            )

            # Start getting all qty
            s = 0
            s1 = 0
            s2 = 0
            for warehouse in warehouses:
                warehousee = warehouse.name
                total_qty = frappe.db.sql(
                    """select
                                                    qty_after_transaction as res
                                                    from `tabStock Ledger Entry` left join `tabWarehouse` on `tabStock Ledger Entry`.warehouse = `tabWarehouse`.name
                                                    where
                                                    `tabStock Ledger Entry`.item_code = %s
                                                    and `tabStock Ledger Entry`.warehouse = %s
                                                    and `tabStock Ledger Entry`.posting_date >= %s
                                                    and `tabStock Ledger Entry`.is_cancelled = 0
                                                    """,
                    (item, warehousee, from_date),
                    as_dict=1,
                )
                for tqty in total_qty:
                    s += tqty.res

                    # Start getting summary qty

                summary_qty = frappe.db.sql(
                    """select
                                                                qty_after_transaction as res
                                                                from `tabStock Ledger Entry` left join `tabWarehouse` on `tabStock Ledger Entry`.warehouse = `tabWarehouse`.name
                                                                where
                                                                `tabStock Ledger Entry`.item_code = %s
                                                                and `tabStock Ledger Entry`.warehouse = %s
                                                                and `tabWarehouse`.summery_stock = 1
                                                                and `tabStock Ledger Entry`.posting_date >= %s
                                                                and `tabStock Ledger Entry`.is_cancelled = 0
                                                                """,
                    (item, warehousee, from_date),
                    as_dict=1,
                )
                for tqty1 in summary_qty:
                    s1 += tqty1.res

                    # Start getting summary qty

                not_summary_qty = frappe.db.sql(
                    """select
                                                                qty_after_transaction as res
                                                                from `tabStock Ledger Entry` left join `tabWarehouse` on `tabStock Ledger Entry`.warehouse = `tabWarehouse`.name
                                                                where
                                                                `tabStock Ledger Entry`.item_code = %s
                                                                and `tabStock Ledger Entry`.warehouse = %s
                                                                and `tabWarehouse`.summery_stock = 0
                                                                and `tabStock Ledger Entry`.posting_date >= %s
                                                                and `tabStock Ledger Entry`.is_cancelled = 0
                                                                """,
                    (item, warehousee, from_date),
                    as_dict=1,
                )
                for tqty2 in not_summary_qty:
                    s2 += tqty2.res

                data["total_qty"] = s
                data["summary_qty"] = s1
                data["not_summary_qty"] = s2
                data["total_value"] = s * item_dict.valuation_rate

            result.append(data)

    return result
