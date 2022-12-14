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
            "label": _("Template"),
            "fieldname": "template",
            "fieldtype": "Link",
            "options": "Journal Entry",
            "width": 130
        },
        {
            "label": _("Jan"),
            "fieldname": "jan",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": _("Feb"),
            "fieldname": "feb",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": _("Mar"),
            "fieldname": "mar",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": _("Apr"),
            "fieldname": "apr",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": _("May"),
            "fieldname": "may",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": _("Jun"),
            "fieldname": "jun",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": _("Jul"),
            "fieldname": "jul",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": _("Aug"),
            "fieldname": "aug",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": _("Sep"),
            "fieldname": "sep",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": _("Oct"),
            "fieldname": "oct",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": _("Nov"),
            "fieldname": "nov",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": _("Dec"),
            "fieldname": "dec",
            "fieldtype": "Data",
            "width": 130
        },

    ]


def get_data(filters, columns):
    year = filters.get('year')
    item_results = frappe.db.sql(f"""
        SELECT distinct
                    template_title as template
                    from
                    `tabJournal Entry Template`
                    where `tabJournal Entry Template`. name IN ('قطع غيار محليه / داخليه', 'قطع غيار توالف', 'قطع غيار توالف')
    """,as_dict=1)
    result = []
    if item_results:
        for item_dict in item_results:
            data = {
                    'template': (item_dict.template),
                }
            template = item_dict.template
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

            jan = frappe.db.sql(f"""select
                                                ifnull(sum(`tabJournal Entry`.total_debit),0) as total_debit
                                                from `tabJournal Entry`
                                                where
                                                `tabJournal Entry`.from_template ='{template}'
                                                and `tabJournal Entry`.posting_date < "{year}-02-01"
                                                """, as_dict=1)
            for tqty in jan:
                s1 = tqty.total_debit
            data['jan'] = s1

            ###########################################################################################
            feb = frappe.db.sql("""select
                                                ifnull(sum(`tabJournal Entry`.total_debit),0) as res
                                                from `tabJournal Entry`
                                                where
                                                `tabJournal Entry`.from_template ='{template}'
                                                and `tabJournal Entry`.posting_date >= "{year}-02-01"
                                                and `tabJournal Entry`.posting_date < "{year}-03-01"
                                                """.format(template=template, year=year), as_dict=1)
            for tqty in feb:
                s2 = tqty.res
            data['feb'] = s2
            ##############################################################################################
            mar = frappe.db.sql("""select
                                                ifnull(sum(`tabJournal Entry`.total_debit),0) as res
                                                from `tabJournal Entry`
                                                where
                                                `tabJournal Entry`.from_template ='{template}'
                                                and `tabJournal Entry`.posting_date >= "{year}-03-01"
                                                and `tabJournal Entry`.posting_date < "{year}-04-01"
                                                """.format(template=template, year=year), as_dict=1)
            for tqty in mar:
                s3 = tqty.res
            data['mar'] = s3
            ###########################################################################################
            apr = frappe.db.sql("""select
                                                ifnull(sum(`tabJournal Entry`.total_debit),0) as res
                                                from `tabJournal Entry`
                                                where
                                                `tabJournal Entry`.from_template ='{template}'
                                                and `tabJournal Entry`.posting_date >= "{year}-04-01"
                                                and `tabJournal Entry`.posting_date < "{year}-05-01"
                                                """.format(template=template, year=year), as_dict=1)
            for tqty in apr:
                s4 = tqty.res
            data['apr'] = s4
            ###########################################################################################
            may = frappe.db.sql("""select
                                                ifnull(sum(`tabJournal Entry`.total_debit),0) as res
                                                from `tabJournal Entry`
                                                where
                                                `tabJournal Entry`.from_template ='{template}'
                                                and `tabJournal Entry`.posting_date >= "{year}-05-01"
                                                and `tabJournal Entry`.posting_date < "{year}-06-01"
                                                """.format(template=template, year=year), as_dict=1)
            for tqty in may:
                s5 = tqty.res
            data['may'] = s5

                # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
            jun = frappe.db.sql("""select
                                            ifnull(sum(`tabJournal Entry`.total_debit),0) as res
                                            from `tabJournal Entry`
                                            where
                                            `tabJournal Entry`.from_template ='{template}'
                                            and `tabJournal Entry`.posting_date >= "{year}-06-01"
                                            and `tabJournal Entry`.posting_date < "{year}-07-01"
                                            """.format(template=template, year=year), as_dict=1)
            for tqty in jun:
                s6 = tqty.res
            data['jun'] = s6

            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
            jul = frappe.db.sql("""select
                                            ifnull(sum(`tabJournal Entry`.total_debit),0) as res
                                            from `tabJournal Entry`
                                            where
                                            `tabJournal Entry`.from_template ='{template}'
                                            and `tabJournal Entry`.posting_date >= "{year}-07-01"
                                            and `tabJournal Entry`.posting_date < "{year}-08-01"
                                            """.format(template=template, year=year), as_dict=1)
            for tqty in jul:
                s7 = tqty.res
            data['jul'] = s7

            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
            aug = frappe.db.sql("""select
                                            ifnull(sum(`tabJournal Entry`.total_debit),0) as res
                                            from `tabJournal Entry`
                                            where
                                            `tabJournal Entry`.from_template ='{template}'
                                            and `tabJournal Entry`.posting_date >= "{year}-08-01"
                                            and `tabJournal Entry`.posting_date < "{year}-09-01"
                                            """.format(template=template, year=year), as_dict=1)
            for tqty in aug:
                s8 = tqty.res
            data['aug'] = s8

            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
            sep = frappe.db.sql("""select
                                            ifnull(sum(`tabJournal Entry`.total_debit),0) as res
                                            from `tabJournal Entry`
                                            where
                                            `tabJournal Entry`.from_template ='{template}'
                                            and `tabJournal Entry`.posting_date >= "{year}-09-01"
                                            and `tabJournal Entry`.posting_date < "{year}-10-01"
                                            """.format(template=template, year=year), as_dict=1)
            for tqty in sep:
                s9 = tqty.res
            data['sep'] = s9

            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
            oct = frappe.db.sql("""select
                                            ifnull(sum(`tabJournal Entry`.total_debit),0) as res
                                            from `tabJournal Entry`
                                            where
                                            `tabJournal Entry`.from_template ='{template}'
                                            and `tabJournal Entry`.posting_date >= "{year}-10-01"
                                            and `tabJournal Entry`.posting_date < "{year}-11-01"
                                            """.format(template=template, year=year), as_dict=1)
            for tqty in oct:
                s10 = tqty.res
            data['oct'] = s10

            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
            nov = frappe.db.sql("""select
                                            ifnull(sum(`tabJournal Entry`.total_debit),0) as res
                                            from `tabJournal Entry`
                                            where
                                            `tabJournal Entry`.from_template ='{template}'
                                            and `tabJournal Entry`.posting_date >= "{year}-11-01"
                                            and `tabJournal Entry`.posting_date < "{year}-12-01"
                                            """.format(template=template, year=year), as_dict=1)
            for tqty in nov:
                s11 = tqty.res
            data['nov'] = s11

            # ///////////////////////////////////////////////////////////////////////////////////////////////////////////
            dec = frappe.db.sql("""select
                                            ifnull(sum(`tabJournal Entry`.total_debit),0) as res
                                            from `tabJournal Entry`
                                            where
                                            `tabJournal Entry`.from_template ='{template}'
                                            and `tabJournal Entry`.posting_date >= "{year}-12-01"
                                            and `tabJournal Entry`.posting_date <= "{year}-12-31"
                                            """.format(template=template, year=year), as_dict=1)
            for tqty in dec:
                s12 = tqty.res
            data['dec'] = s12

            result.append(data)
    return result


def get_item_price_qty_data(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " and `tabJournal Entry`.posting_date>=%(from_date)s"
    if filters.get("to_date"):
        conditions += " and `tabJournal Entry`.posting_date<=%(to_date)s"
    if filters.get("account"):
        conditions += " and `tabJournal Entry Account`.account =%(account)s"
    if filters.get("from_template"):
        conditions += " and `tabJournal Entry`.from_template =%(from_template)s"

    item_results = frappe.db.sql("""
                select
                        `tabJournal Entry`.name as name,
                        `tabJournal Entry`.posting_date as posting_date,
                         `tabJournal Entry Account`.account as account,
                        `tabJournal Entry`.from_template as from_template,
                        `tabJournal Entry Account`.debit_in_account_currency as debit_in_account_currency



                from
                        `tabJournal Entry` join `tabJournal Entry Account` on `tabJournal Entry`.name = `tabJournal Entry Account`.parent
                where
                        `tabJournal Entry`.docstatus = 1
                        and `tabJournal Entry`.from_template in ("قطع غيار محليه / داخليه","قطع غيار توالف","قطع غيار جديده")
                        and `tabJournal Entry Account`.account in ("قطع غيار جديده - IBC","قطع غيار توالف - IBC","قطع غيار محليه / داخليه - IBC")
                {conditions}
                """.format(conditions=conditions), filters, as_dict=1)

    # price_list_names = list(set([item.price_list_name for item in item_results]))

    # buying_price_map = get_price_map(price_list_names, buying=1)
    # selling_price_map = get_price_map(price_list_names, selling=1)

    result = []
    if item_results:
        for item_dict in item_results:
            data = {
                'name': item_dict.name,
                'posting_date': item_dict.posting_date,
                'account': item_dict.account,
                'debit_in_account_currency': item_dict.debit_in_account_currency,
                'from_template': item_dict.from_template,


            }
            result.append(data)

    return result
