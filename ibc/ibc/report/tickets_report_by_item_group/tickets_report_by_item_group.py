# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns(filters)

    if filters.get('year'):
        year = filters.get('year')
        item_results = frappe.db.sql("""
            SELECT distinct
                    item_group as item_group
                    from
                    `tabTicket Items`
                    where 
                        item_group is not null
                        order by item_group
                """, filters, as_dict=1)


        result = []
        if item_results:
            for item_dict in item_results:

                data = {
                    'item_group': (item_dict.item_group),
                }
                to_date = filters.get("to_date")
                from_date = filters.get("from_date")
                item_groups = item_dict.item_group

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
                                                ifnull(sum(cost),0) as res
                                                from `tabTicket Items` join `tabTicket` on `tabTicket Items`.parent = `tabTicket`.name
                                                where
                                                `tabTicket Items`.item_group ='{item_groups}'
                                                and `tabTicket`.posting_date < "{year}-02-01"
                                                and `tabTicket`.posting_date >= "{year}-01-01"
                                                and `tabTicket`.docstatus = 1
                                                """.format(item_groups=item_groups, year=year), as_dict=1)
                for tqty in jan:
                    s1 += tqty.res
                data['jan'] = s1

                # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
                feb = frappe.db.sql("""select
                                                ifnull(sum(cost),0) as res
                                                from `tabTicket Items` join `tabTicket` on `tabTicket Items`.parent = `tabTicket`.name
                                                where
                                                `tabTicket Items`.item_group ='{item_groups}'
                                                and `tabTicket`.posting_date < "{year}-03-01"
                                                and `tabTicket`.posting_date >= "{year}-02-01"
                                                and `tabTicket`.docstatus = 1
                                                """.format(item_groups=item_groups, year=year), as_dict=1)
                for tqty in feb:
                    s2 += tqty.res
                data['feb'] = s2

                # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
                mar = frappe.db.sql("""select
                                                ifnull(sum(cost),0) as res
                                                from `tabTicket Items` join `tabTicket` on `tabTicket Items`.parent = `tabTicket`.name
                                                where
                                                `tabTicket Items`.item_group ='{item_groups}'
                                                and `tabTicket`.posting_date < "{year}-04-01"
                                                and `tabTicket`.posting_date >= "{year}-03-01"
                                                and `tabTicket`.docstatus = 1
                                                """.format(item_groups=item_groups, year=year), as_dict=1)
                for tqty in mar:
                    s3 += tqty.res
                data['mar'] = s3

                # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
                apr = frappe.db.sql("""select
                                                ifnull(sum(cost),0) as res
                                                from `tabTicket Items` join `tabTicket` on `tabTicket Items`.parent = `tabTicket`.name
                                                where
                                                `tabTicket Items`.item_group ='{item_groups}'
                                                and `tabTicket`.posting_date < "{year}-05-01"
                                                and `tabTicket`.posting_date >= "{year}-04-01"
                                                and `tabTicket`.docstatus = 1
                                                """.format(item_groups=item_groups, year=year), as_dict=1)
                for tqty in apr:
                    s4 += tqty.res
                data['apr'] = s4

                # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
                may = frappe.db.sql("""select
                                                ifnull(sum(cost),0) as res
                                                from `tabTicket Items` join `tabTicket` on `tabTicket Items`.parent = `tabTicket`.name
                                                where
                                                `tabTicket Items`.item_group ='{item_groups}'
                                                and `tabTicket`.posting_date < "{year}-06-01"
                                                and `tabTicket`.posting_date >= "{year}-05-01"
                                                and `tabTicket`.docstatus = 1
                                                """.format(item_groups=item_groups, year=year), as_dict=1)
                for tqty in may:
                    s5 += tqty.res
                data['may'] = s5

                # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
                jun = frappe.db.sql("""select
                                                 ifnull(sum(cost),0) as res
                                                from `tabTicket Items` join `tabTicket` on `tabTicket Items`.parent = `tabTicket`.name
                                                where
                                                `tabTicket Items`.item_group ='{item_groups}'
                                                and `tabTicket`.posting_date < "{year}-07-01"
                                                and `tabTicket`.posting_date >= "{year}-06-01"
                                                and `tabTicket`.docstatus = 1
                                                """.format(item_groups=item_groups, year=year), as_dict=1)
                for tqty in jun:
                    s6 += tqty.res
                data['jun'] = s6

                # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
                jul = frappe.db.sql("""select
                                                 ifnull(sum(cost),0) as res
                                                from `tabTicket Items` join `tabTicket` on `tabTicket Items`.parent = `tabTicket`.name
                                                where
                                                `tabTicket Items`.item_group ='{item_groups}'
                                                and `tabTicket`.posting_date < "{year}-08-01"
                                                and `tabTicket`.posting_date >= "{year}-07-01"
                                                and `tabTicket`.docstatus = 1
                                                """.format(item_groups=item_groups, year=year), as_dict=1)
                for tqty in jul:
                    s7 += tqty.res
                data['jul'] = s7

                # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
                aug = frappe.db.sql("""select
                                                 ifnull(sum(cost),0) as res
                                                from `tabTicket Items` join `tabTicket` on `tabTicket Items`.parent = `tabTicket`.name
                                                where
                                                `tabTicket Items`.item_group ='{item_groups}'
                                                and `tabTicket`.posting_date < "{year}-09-01"
                                                and `tabTicket`.posting_date >= "{year}-08-01"
                                                and `tabTicket`.docstatus = 1
                                                """.format(item_groups=item_groups, year=year), as_dict=1)
                for tqty in aug:
                    s8 += tqty.res
                data['aug'] = s8

                # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
                sep = frappe.db.sql("""select
                                                ifnull(sum(cost),0) as res
                                                from `tabTicket Items` join `tabTicket` on `tabTicket Items`.parent = `tabTicket`.name
                                                where
                                                `tabTicket Items`.item_group ='{item_groups}'
                                                and `tabTicket`.posting_date < "{year}-10-01"
                                                and `tabTicket`.posting_date >= "{year}-09-01"
                                                and `tabTicket`.docstatus = 1
                                                """.format(item_groups=item_groups, year=year), as_dict=1)
                for tqty in sep:
                    s9 += tqty.res
                data['sep'] = s9

                # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
                oct = frappe.db.sql("""select
                                                ifnull(sum(cost),0) as res
                                                from `tabTicket Items` join `tabTicket` on `tabTicket Items`.parent = `tabTicket`.name
                                                where
                                                `tabTicket Items`.item_group ='{item_groups}'
                                                and `tabTicket`.posting_date < "{year}-11-01"
                                                and `tabTicket`.posting_date >= "{year}-10-01"
                                                and `tabTicket`.docstatus = 1
                                                """.format(item_groups=item_groups, year=year), as_dict=1)
                for tqty in oct:
                    s10 += tqty.res
                data['oct'] = s10

                # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
                nov = frappe.db.sql("""select
                                                ifnull(sum(cost),0) as res
                                                from `tabTicket Items` join `tabTicket` on `tabTicket Items`.parent = `tabTicket`.name
                                                where
                                                `tabTicket Items`.item_group ='{item_groups}'
                                                and `tabTicket`.posting_date < "{year}-12-01"
                                                and `tabTicket`.posting_date >= "{year}-11-01"
                                                and `tabTicket`.docstatus = 1
                                                """.format(item_groups=item_groups, year=year), as_dict=1)
                for tqty in nov:
                    s11 += tqty.res
                data['nov'] = s11

                # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
                dec = frappe.db.sql("""select
                                                ifnull(sum(cost),0) as res
                                                from `tabTicket Items` join `tabTicket` on `tabTicket Items`.parent = `tabTicket`.name
                                                where
                                                `tabTicket Items`.item_group ='{item_groups}'
                                                and `tabTicket`.posting_date <= "{year}-12-31"
                                                and `tabTicket`.posting_date >= "{year}-12-01"
                                                and `tabTicket`.docstatus = 1
                                                """.format(item_groups=item_groups, year=year), as_dict=1)
                for tqty in dec:
                    s12 += tqty.res
                data['dec'] = s12

                # ///////////////////////////////////////////////////////////////////////////////////////////////////////////

                result.append(data)

            return columns, result



def get_columns(filters):
    if filters.get('year'):
        return [
            {
                "label": _("Item Group"),
                "fieldname": "item_group",
                "fieldtype": "Data",
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