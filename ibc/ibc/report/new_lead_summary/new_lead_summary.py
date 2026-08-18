from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"fieldname": "lead_name", "label": _("Persone Name"), "fieldtype": "Data", "width": 150},
        {"fieldname": "name", "label": _("Lead No"), "fieldtype": "Link", "options": "Lead", "width": 200},
        {"fieldname": "company_name", "label": _("Company Name"), "fieldtype": "Data", "width": 150},
        {"fieldname": "lead_status", "label": _("Lead Status"), "fieldtype": "Data", "width": 120},
        {"fieldname": "lead_owner", "label": _("Lead Owner"), "fieldtype": "Data", "width": 150},
        {"fieldname": "status", "label": _("Status"), "fieldtype": "Data", "width": 120},
        {"fieldname": "date", "label": _("Date"), "fieldtype": "Data", "width": 100},
        {"fieldname": "source", "label": _("Source"), "fieldtype": "Data", "width": 100},
        {"fieldname": "system_type", "label": _("System Type"), "fieldtype": "Link", "options": "System Type", "width": 120},
        {"fieldname": "sales_person", "label": _("Sales Person"), "fieldtype": "Link", "options": "Sales Person", "width": 150},
        {"fieldname": "zone", "label": _("Zone"), "fieldtype": "Link", "options": "Zone", "width": 120},
        {"fieldname": "city", "label": _("City"), "fieldtype": "Data", "width": 120},
        {"fieldname": "phone", "label": _("Phone"), "fieldtype": "Data", "width": 120},
        {"fieldname": "notes", "label": _("Notes"), "fieldtype": "Data", "width": 200},
        {"fieldname": "customer", "label": _("Customer"), "fieldtype": "Link", "options": "Customer", "width": 150},
        {"fieldname": "customer_group", "label": _("Customer Group"), "fieldtype": "Link", "options": "Customer Group", "width": 150},
        {"fieldname": "mobile_no", "label": _("Mobile No"), "fieldtype": "Data", "width": 100},
        {"fieldname": "orders", "label": _("Orders"), "fieldtype": "Currency", "width": 100},
    ]


def get_data(filters):
    filters = filters or {}

    return frappe.db.sql(
        """
        select distinct
            `tabLead`.lead_name as lead_name,
            `tabLead`.name as name,
            `tabLead`.company_name as company_name,
            `tabLead`.lead_status as lead_status,
            (
                select `tabUser`.full_name
                from `tabUser`
                where `tabUser`.name = `tabLead`.lead_owner
            ) as lead_owner,
            `tabLead`.status as status,
            DATE(`tabLead`.creation) as date,
            `tabLead`.source as source,
            `tabLead`.system_type as system_type,
            `tabLead`.sales_person as sales_person,
            `tabLead`.custom_zone as zone,
            `tabLead`.custom_new_city as city,
            `tabLead`.phone as phone,
            `tabCRM Note`.note as notes,
            `tabCustomer`.name as customer,
            `tabCustomer`.customer_group as customer_group,
            ifnull(
                `tabLead`.mobile_no,
                (
                    select `tabContact`.mobile_no
                    from `tabContact`
                    inner join `tabDynamic Link`
                        on `tabDynamic Link`.parent = `tabContact`.name
                    where `tabDynamic Link`.link_name = `tabLead`.name
                    limit 1
                )
            ) as mobile_no,
            (
                select sum(`tabSales Order`.base_grand_total)
                from `tabSales Order`
                where `tabSales Order`.customer = `tabCustomer`.name
                    and `tabSales Order`.docstatus = 1
            ) as orders

        from `tabLead`
        left join `tabCustomer`
            on `tabCustomer`.lead_name = `tabLead`.name
        left join `tabCRM Note`
            on `tabCRM Note`.parent = `tabLead`.name

        where DATE(`tabLead`.creation) between %(from_date)s and %(to_date)s
        """,
        filters,
        as_dict=True,
    )
