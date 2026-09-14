from __future__ import unicode_literals
import frappe
from frappe import _
from ibc.ibc.utils.customer_contact import sync_customer_mobile_no


def before_insert(doc, method=None):
    pass

def after_insert(doc, method=None):
    pass

def onload(doc, method=None):
    pass

def before_validate(doc, method=None):
    pass

def validate(doc, method=None):
    if doc.quotation_to == "Customer" and not doc.custom_mobile_no and doc.party_name:
        doc.custom_mobile_no = get_mobile_no_from_lead(doc.party_name)

    if doc.quotation_to == "Customer" and not doc.custom_mobile_no:
        frappe.throw(
            _('لا يمكنك الاستمرار في عرض السعر هذا حتى تقوم بتعيين رقم الموبايل للعميل "{0}"').format(
                doc.customer_name or doc.party_name
            ),
            title=_("رقم الموبايل مطلوب"),
        )


def get_mobile_no_from_lead(customer):
    """Fallback: if the Customer has no mobile no, try the Lead it was converted from."""
    lead = frappe.db.get_value("Customer", customer, "lead_name")
    return lead and frappe.db.get_value("Lead", lead, "mobile_no")

def on_submit(doc, method=None):
    pass

def on_cancel(doc, method=None):
    pass

def on_update_after_submit(doc, method=None):
    pass

def before_save(doc, method=None):
    pass

def before_cancel(doc, method=None):
    pass

def on_update(doc, method=None):
    if doc.quotation_to == "Customer" and doc.party_name and doc.has_value_changed("custom_mobile_no"):
        sync_customer_mobile_no(doc.party_name, doc.custom_mobile_no)

def before_rename(doc, method, old, new, merge=False):
    if frappe.session.user == "Administrator":
        return

    roles = set(frappe.get_roles(frappe.session.user))
    if "Sales User" in roles and not roles & {"System Manager", "Sales Manager"}:
        frappe.throw(
            _("You are not permitted to edit the ID of this Quotation. Please contact your Sales Manager or System Manager."),
            frappe.PermissionError,
        )
