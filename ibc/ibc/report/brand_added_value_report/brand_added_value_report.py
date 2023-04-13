# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import datetime
import numbers
from frappe.utils import flt


def execute(filters=None):
    data = Data_Collector(filters).get_data()
    columns = get_columns()
    return columns, data


class Dict_Operator:
    def __init__(self):
        pass

    def subtract(self, first: dict, second: dict):
        result = {}
        brands = list(first.keys()) + list(second.keys())
        for brand in brands:
            result[brand] = first.get(brand, 0) - second.get(brand, 0)
        return result

    def add(self, first: dict, second: dict):
        result = {}
        brands = list(first.keys()) + list(second.keys())
        for brand in brands:
            result[brand] = first.get(brand, 0) + second.get(brand, 0)
        return result

    def divide(self, first: dict, second: dict):
        result = {}
        brands = list(first.keys()) + list(second.keys())
        for brand in brands:
            if second.get(brand, 0):
                result[brand] = first.get(brand, 0) / second.get(brand)
            else:
                result[brand] = 0
        return result

    def merge_from_into_with_name(self, source: dict, destination: dict,  column: str):
        # key is brand name
        for key, value in source.items():
            if key not in destination:
                destination[key] = {}
            destination[key][column] = value
            # destination[key][column] = flt(value) if isinstance(
            #     value, numbers.Number) else value

    def merge_all_data_around_key(self, data: dict):
        result = {}
        for column in data:  # column name is the key in data dictionary
            # data[column] is a dictionary where brand is the key
            self.merge_from_into_with_name(
                data[column], result, column)
        return result

    def flatten(self, listOfDict, key, key_of_value):
        result = {}
        for obj in listOfDict:
            result[obj[key]] = obj[key_of_value]
        return result


class Data_Collector:
    def __init__(self, filters={}):
        self._filters = filters
        if self._filters is None:
            self._filters = {}
        self._common_conditions = self._get_common_conditions(self._filters)
        self._dict_operator = Dict_Operator()

    def _get_common_conditions(self, filters: dict):
        conditions = []
        conditions.append("1 = 1")

        if 'from_date' in filters:
            conditions.append(f"creation >= {filters.get('from_date')}")

        if 'to_date' in filters:
            conditions.append(f"creation <= {filters.get('to_date')}")

        return " and ".join(conditions)

    def _get_brands(self):
        brands = frappe.db.sql("""select brand from `tabBrand`""", as_dict=1)
        brands = self._dict_operator.flatten(brands, 'brand', 'brand')
        return brands

    def _get_purchases(self):
        purchase = frappe.db.sql(
            """SELECT
                    brand,
                    sum(amount) as purchase
                FROM
                    `tabPurchase Invoice Item` as item
                    inner join
                    `tabPurchase Invoice` as invoice
                    on
                    invoice.name = item.parent
                WHERE
                    invoice.posting_date between %s and %s
                    and invoice.status != 'Cancelled'
                GROUP BY
                    brand""",
            (self._filters.get('from_date'), self._filters.get('to_date')),
            as_dict=1)
        purchase = self._dict_operator.flatten(
            purchase, 'brand', 'purchase')
        return purchase

    def _get_sales(self):
        sales = frappe.db.sql("""SELECT
                                    brand,
                                    sum(amount) as sales_value 
                                FROM
                                    `tabSales Invoice Item` as item
                                    inner join
                                    `tabSales Invoice` as invoice
                                ON
                                    invoice.name = item.parent
                                WHERE
                                    invoice.posting_date between %s and %s
                                    and invoice.status != 'Cancelled'
                                GROUP BY
                                    brand""",
                              (self._filters.get('from_date'),
                               self._filters.get('to_date')),
                              as_dict=1)
        sales = self._dict_operator.flatten(sales, "brand", "sales_value")
        return sales

    def _get_opening(self):
        # opening = frappe.db.sql("""
        # SELECT
        #     brand,
        #     sum(actual_qty) as opening
        # FROM
        #     `tabStock Ledger Entry`
        # WHERE
        #     creation < %s
        #     and is_cancelled = 0
        # GROUP BY
        #     brand
        # """, (self._filters.get('from_date')), as_dict=1)

        # opening = frappe.db.sql("""select
        #                         brand,
        # 						qty_after_transaction  as opening
        # 						from `tabStock Ledger Entry`
        # 						and `tabStock Ledger Entry`.posting_date <= %s
        # 						and `tabStock Ledger Entry`.is_cancelled = 0
        #                         and `tabStock  Ledger Entry`.brand = 'Terofire'
        # 						ORDER BY `tabStock Ledger Entry`.posting_date DESC, `tabStock Ledger Entry`.posting_time DESC , `tabStock Ledger Entry`.creation DESC LIMIT 1""",

        #                         (item, warehousee, from_date), as_dict=1)

        # opening = frappe.db.sql("""
        #         # select
        #         #   brand,
        #         #   sum(actual_qty * valuation_rate) as opening
        #         # from
        #         #   `tabStock Ledger Entry`
        #         # where posting_date < %s
        #         # group by
        #         #   brand
        #         # """, (self._filters.get('from_date')), as_dict=1)
        # opening = self._dict_operator.flatten(opening, "brand", "opening")
        # return opening
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

            # condition = x.get('qty_after_transaction', 0) == y.get(
            #     'qty_after_transaction', 0) and x.get('valuation_rate', 0) == y.get('valuation_rate', 0)

            # if condition is False:
            #     assert x.get('item_code', '') == y.get(
            #         'item_code', ''), "invalid 1"
            #     assert x.get('brand', '') == y.get(
            #         'brand', ''), "invalid 2"
            #     assert x.get('warehouse', '') == y.get(
            #         'warehouse', ''), "invalid 3"

            # z = x
            # z['qty_after_transaction'] = (x.get(
            #     'qty_after_transaction', 0) + y.get('qty_after_transaction', 0)) / 2
            # z['valuation_rate'] = (x.get(
            #     'valuation_rate', 0) + y.get('valuation_rate', 0)) / 2
            # return z
            # assert condition, "invalid 4"

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
                            """, (self._filters.get('from_date')), as_dict=1)

        lookup = {}
        for stock in stocks:
            if (stock.item_code, stock.warehouse) not in lookup:
                lookup[(stock.item_code, stock.warehouse)] = stock
            else:
                lookup[(stock.item_code, stock.warehouse)] = get_best(
                    lookup[(stock.item_code, stock.warehouse)], stock)

        opening = {}
        for key, value in lookup.items():
            opening[value.brand] = opening.get(
                value.brand, 0) + value['qty_after_transaction'] * value['valuation_rate']
        return opening

    def _get_current_value(self):
        # result = frappe.db.sql(f"""
        #                         select
        #                             brand,
        #                             sum(stock_value) as current_value
        #                         from
        #                             `tabBin`
        #                         group by
        #                             brand
        #                         """,
        #                        as_dict=1)
        # result = self._dict_operator.flatten(result, 'brand', 'current_value')
        # return result

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
                            where posting_date <= %s
                                    and is_cancelled = 0
                            """, (self._filters.get('to_date')), as_dict=1)

        lookup = {}
        for stock in stocks:
            if (stock.item_code, stock.warehouse) not in lookup:
                lookup[(stock.item_code, stock.warehouse)] = stock
            else:
                lookup[(stock.item_code, stock.warehouse)] = get_best(
                    lookup[(stock.item_code, stock.warehouse)], stock)

        opening = {}
        for key, value in lookup.items():
            opening[value.brand] = opening.get(
                value.brand, 0) + value['qty_after_transaction'] * value['valuation_rate']
        return opening

    def _calculate_total_in(self, opening: dict, purchase: dict):
        return self._dict_operator.add(opening, purchase)

    def _calculate_cogs(self, total_in: dict, purchase: dict):
        return self._dict_operator.subtract(total_in, purchase)

    def _calculate_added_value(self, sales: dict, cogs: dict):
        return self._dict_operator.subtract(sales, cogs)

    def _calculate_cogs__sales_value(self, cogs: dict, sales: dict):
        return self._dict_operator.divide(cogs, sales)

    def _calculate_added_value__sales(self, added_value: dict, sales: dict):
        return self._dict_operator.divide(added_value, sales)

    def _calculate_added_value__cogs(self, added_value: dict, cogs: dict):
        return self._dict_operator.divide(added_value, cogs)

    def get_data(self):
        data = {}
        brand = data['brand'] = self._get_brands()
        purchases = data['purchase'] = self._get_purchases()
        sales = data['sales_value'] = self._get_sales()
        opening = data['opening'] = self._get_opening()
        current_value = data['current_value'] = self._get_current_value()

        total_in = data['total_in'] = self._calculate_total_in(
            opening, purchases)
        cogs = data['cogs'] = self._calculate_cogs(total_in, current_value)
        added_value = data['added_value'] = self._calculate_added_value(
            sales, cogs)
        data['cogs/sales_value'] = self._calculate_cogs__sales_value(
            cogs, sales)
        data['added_value/sales_value'] = self._calculate_added_value__sales(
            added_value, sales)
        data['added_value/cogs'] = self._calculate_added_value__cogs(
            added_value, cogs)
        result = self._dict_operator.merge_all_data_around_key(data)
        return list(result.values())


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


# opening = frappe.db.sql("""select
#                                 qty_after_transaction as res,
#                                 valuation_rate as frate,
#                                 stock_value as sv
#                                 from `tabStock Ledger Entry` join `tabWarehouse` on `tabStock Ledger Entry`.warehouse = `tabWarehouse`.name
#                                 where
#                                 `tabStock Ledger Entry`.item_code = %s
#                                 and `tabStock Ledger Entry`.warehouse = %s
#                                 and `tabStock Ledger Entry`.posting_date <= %s
#                                 and `tabStock Ledger Entry`.is_cancelled = 0
#                                 ORDER BY `tabStock Ledger Entry`.posting_date DESC, `tabStock Ledger Entry`.posting_time DESC , `tabStock Ledger Entry`.creation DESC LIMIT 1""",
#                                             (item, warehousee, from_date), as_dict=1)

