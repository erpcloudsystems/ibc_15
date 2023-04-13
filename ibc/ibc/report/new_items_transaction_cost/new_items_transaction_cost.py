# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
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


def get_data(filters):
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def hash_query(filters, doctype, sum_of, conditions):
    return frappe._dict(frappe.db.sql(
        """
            select 
                `tabStock Ledger Entry`.item_code, sum({sum_of}) as sum
            from
                `tabStock Ledger Entry`  
                join `tabWarehouse` 
                on `tabWarehouse`.name = `tabStock Ledger Entry`.warehouse
            where
                `tabStock Ledger Entry`.voucher_type = "{doctype}"
                and `tabStock Ledger Entry`.posting_date >= "{from_date}"
                and `tabStock Ledger Entry`.posting_date <= "{to_date}"
                and {conditions}
                and `tabStock Ledger Entry`.is_cancelled = 0
            GROUP BY 
                `tabStock Ledger Entry`.item_code
            """.format(doctype=doctype, sum_of=sum_of, conditions=conditions, from_date=filters.get("from_date"), to_date=filters.get("to_date"))))


# def retransform(item_qty_in_allWarehouses1, item_valuationRate_in_allWarehouses1):
#     body = {}
#     for row in item_qty_in_allWarehouses1:
#         body[row.item_code] = {
#             "actual_qty": row.actual_qty,
#         }
#     for row in item_valuationRate_in_allWarehouses1:
#         body[row.item_code]["valuation_rate"] = row.valuation_rate

#     return body


def get_item_price_qty_data(filters):

    delivered = hash_query(filters, "Delivery Note", "actual_qty",
                           conditions=" `tabStock Ledger Entry`.actual_qty < 0")
    delivered_v = hash_query(filters, "Delivery Note", "stock_value_difference",
                             conditions=" `tabStock Ledger Entry`.actual_qty <0 ")
    sales_return = hash_query(filters, "Sales Invoice", "actual_qty",
                              conditions=" `tabStock Ledger Entry`.actual_qty >0 ")
    purchase = hash_query(filters, "Purchase Invoice", "actual_qty",
                          conditions=" `tabStock Ledger Entry`.actual_qty > 0")
    purchase_return = hash_query(filters, "Purchase Invoice", "actual_qty",
                                 conditions=" `tabStock Ledger Entry`.actual_qty < 0")
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

    # new_item_qty_in_allWarehouses = retransform(
    #     item_qty_in_allWarehouses, item_valuationRate_in_allWarehouses)

    # item_qty_in_allWarehouses_balance_lessthan = frappe.db.sql("""select
    # 						item_code,
    # 						sum(actual_qty) as actual_qty
    # 						from `tabStock Ledger Entry`
    # 						WHERE `tabStock Ledger Entry`.posting_date <= "{to_date}"
    # 						GROUP BY item_code""".format(to_date=filters.get("to_date")), as_dict=1)
    # item_valuationRate_balance_allWarehouses = frappe.db.sql("""select
    # 						item_code,
    # 						AVG(valuation_rate)  as valuation_rate
    # 						from `tabStock Ledger Entry`
    # 						WHERE `tabStock Ledger Entry`.posting_date <= "{to_date}"
    # 						and `tabStock Ledger Entry`.is_cancelled = 0
    # 						GROUP BY item_code""".format(to_date=filters.get("to_date")), as_dict=1)
    balance, balance_v = get_balance_and_balance_v(filters)

    sales_in_qty = frappe._dict(frappe.db.sql("""
                            select
    			    			item_code,
    	    					SUM(actual_qty * valuation_rate) as sales_in_qty_value
    						from `tabStock Ledger Entry`
    						where 
                                `tabStock Ledger Entry`.voucher_type = "Sales Invoice"
                                and `tabStock Ledger Entry`.actual_qty > 0
                                and `tabStock Ledger Entry`.posting_date >= "{from_date}"
                                and `tabStock Ledger Entry`.posting_date <= "{to_date}"
                                and `tabStock Ledger Entry`.is_cancelled = 0
    						GROUP BY 
                                `tabStock Ledger Entry`.item_code
    						 """.format(from_date=filters.get("from_date"), to_date=filters.get("to_date"))))
    purchase_in_qty = frappe._dict(frappe.db.sql("""select
    						item_code,
    						SUM(actual_qty * valuation_rate) as purchase_in_qty_value
    						from `tabStock Ledger Entry`
    						where  `tabStock Ledger Entry`.voucher_type = "Purchase Invoice"
    						and `tabStock Ledger Entry`.actual_qty > 0
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
    # new_item_qtybalance_in_allWarehouses = retransform(
    #     item_qty_in_allWarehouses_balance_lessthan, item_valuationRate_balance_allWarehouses)

    opening, opening_v = get_opening_and_opening_v(filters)

    result = []
    item_results = frappe.db.sql("""
		SELECT distinct
				`tabItem`.name as item_code,
				`tabItem`.item_name as item_name,
				ifnull(`tabItem`.valuation_rate, 0) as value,
				`tabItem`.brand as brand,
				`tabItem`.item_group as item_group
				from
				`tabItem`
			""", as_dict=1)

    if item_results:
        for item_dict in item_results:
            data = {
                'brand': item_dict.brand,
                'item_code': item_dict.item_code,
                'item_name': item_dict.item_name,
                'item_group': item_dict.item_group,
                'delivered': delivered.get(item_dict.item_code, 0),
                'delivered_v': delivered_v.get(item_dict.item_code, 0),
                'sales_return': sales_return.get(item_dict.item_code, 0),
                'purchase': purchase.get(item_dict.item_code, 0),
                'purchase_return': purchase_return.get(item_dict.item_code, 0)
            }
            data['sales_return_v'] = sales_in_qty.get(item_dict.item_code)
            data['purchase_v'] = purchase_in_qty.get(item_dict.item_code)
            data['purchase_return_v'] = purchase_in_re_qty.get(
                item_dict.item_code)
            data['opening'] = opening.get(item_dict.item_code, 0)
            data['opening_v'] = opening_v.get(item_dict.item_code, 0)
            # data['balance'] = new_item_qtybalance_in_allWarehouses.get(item_dict.item_code).get(
            #     "actual_qty", 0) if new_item_qtybalance_in_allWarehouses.get(item_dict.item_code, 0) else 0
            # data['balance_v'] = new_item_qtybalance_in_allWarehouses.get(item_dict.item_code).get("actual_qty", 0) * new_item_qtybalance_in_allWarehouses.get(
            # item_dict.item_code).get("valuation_rate", 0) if new_item_qtybalance_in_allWarehouses.get(item_dict.item_code, 0) else 0
            data['balance'] = balance.get(item_dict.item_code, 0)
            data['balance_v'] = balance_v.get(item_dict.item_code, 0)
            result.append(data)

    return result


def get_opening_and_opening_v(filters):
    def get_best(x, y):
        if x.get('posting_date', 0) > y.get('posting_date', 0):
            return x
        if x.get('posting_date', 0) < y.get('posting_date', 0):
            return y
        if x.get('posting_time', 0) > y.get('posting_time', 0):
            return x
        if x.get('posting_time', 0) < y.get('posting_time', 0):
            return y

        if x.get('name') > y.get('name'):
            return x

        return y

    stocks = frappe.db.sql("""
                        select
                            name,
                            brand,
                            item_code,
                            warehouse,
                            posting_date,
                            posting_time,
                            qty_after_transaction,
                            valuation_rate
                        from `tabStock Ledger Entry`
                        where posting_date < %s
                                and is_cancelled = 0
                        """, (filters.get('from_date')), as_dict=1)

    lookup = {}
    for stock in stocks:
        if (stock.item_code, stock.warehouse) not in lookup:
            lookup[(stock.item_code, stock.warehouse)] = stock
        else:
            lookup[(stock.item_code, stock.warehouse)] = get_best(
                lookup[(stock.item_code, stock.warehouse)], stock)

    opening = {}
    opening_v = {}
    for key, value in lookup.items():
        item_code = value.item_code
        qty_after_transaction = value.qty_after_transaction
        valuation_rate = value.valuation_rate
        opening[item_code] = opening.get(
            item_code, 0) + qty_after_transaction
        opening_v[item_code] = opening_v.get(
            item_code, 0) + qty_after_transaction * valuation_rate

    return opening, opening_v


def get_balance_and_balance_v(filters):
    def get_best(x, y):
        if x.get('posting_date', 0) > y.get('posting_date', 0):
            return x
        if x.get('posting_date', 0) < y.get('posting_date', 0):
            return y
        if x.get('posting_time', 0) > y.get('posting_time', 0):
            return x
        if x.get('posting_time', 0) < y.get('posting_time', 0):
            return y

        if x.get('name') > y.get('name'):
            return x

        return y

    stocks = frappe.db.sql("""
                        select
                            name,
                            brand,
                            item_code,
                            warehouse,
                            posting_date,
                            posting_time,
                            qty_after_transaction,
                            valuation_rate
                        from `tabStock Ledger Entry`
                        where posting_date <= %(to_date)s
                                and is_cancelled = 0
                        """, (filters), as_dict=1)

    lookup = {}
    for stock in stocks:
        if (stock.item_code, stock.warehouse) not in lookup:
            lookup[(stock.item_code, stock.warehouse)] = stock
        else:
            lookup[(stock.item_code, stock.warehouse)] = get_best(
                lookup[(stock.item_code, stock.warehouse)], stock)

    balance = {}
    balance_v = {}
    for key, value in lookup.items():
        item_code = value.item_code
        qty_after_transaction = value.qty_after_transaction
        valuation_rate = value.valuation_rate
        balance[item_code] = balance.get(
            item_code, 0) + qty_after_transaction
        balance_v[item_code] = balance_v.get(
            item_code, 0) + qty_after_transaction * valuation_rate

    return balance, balance_v

