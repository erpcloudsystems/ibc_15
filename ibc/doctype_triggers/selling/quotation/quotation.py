from __future__ import unicode_literals
import frappe
from frappe import _
from ibc.ibc.utils.customer_contact import sync_customer_mobile_no, get_customer_mobile_no

QUOTATION_MOBILE_NO_PARTY_TYPES = ("Customer", "Lead")


def before_insert(doc, method=None):
    pass

def after_insert(doc, method=None):
    pass

def onload(doc, method=None):
    pass

def before_validate(doc, method=None):
    pass

def validate(doc, method=None):
    if doc.quotation_to in QUOTATION_MOBILE_NO_PARTY_TYPES and not doc.custom_mobile_no and doc.party_name:
        doc.custom_mobile_no = get_party_mobile_no(doc.quotation_to, doc.party_name)

    if doc.quotation_to in QUOTATION_MOBILE_NO_PARTY_TYPES and not doc.custom_mobile_no:
        frappe.throw(
            _('لا يمكنك الاستمرار في عرض السعر هذا حتى تقوم بتعيين رقم الموبايل للعميل "{0}"').format(
                doc.customer_name or doc.party_name
            ),
            title=_("رقم الموبايل مطلوب"),
        )


@frappe.whitelist()
def get_party_mobile_no(quotation_to, party_name):
    """Whitelisted lookup for the client script, covering both party types a
    Quotation can point at. Deliberately ignores permissions (see
    ibc.ibc.utils.customer_contact.get_customer_mobile_no for why).
    """
    if quotation_to == "Customer":
        return get_customer_mobile_no(party_name)
    if quotation_to == "Lead":
        return frappe.db.get_value("Lead", party_name, "mobile_no")
    return None

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
    if not doc.party_name or not doc.custom_mobile_no or not doc.has_value_changed("custom_mobile_no"):
        return

    if doc.quotation_to == "Customer":
        sync_customer_mobile_no(doc.party_name, doc.custom_mobile_no)
    elif doc.quotation_to == "Lead":
        frappe.db.set_value("Lead", doc.party_name, "mobile_no", doc.custom_mobile_no)

def before_rename(doc, method, old, new, merge=False):
    if frappe.session.user == "Administrator":
        return

    roles = set(frappe.get_roles(frappe.session.user))
    if "Sales User" in roles and not roles & {"System Manager", "Sales Manager"}:
        frappe.throw(
            _("You are not permitted to edit the ID of this Quotation. Please contact your Sales Manager or System Manager."),
            frappe.PermissionError,
        )
