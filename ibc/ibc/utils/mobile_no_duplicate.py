from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import get_link_to_form

MAX_DUPLICATES_SHOWN = 5


def find_duplicate_mobile_no_documents(doc):
    """Find every other Lead/Customer already using doc.mobile_no.

    Excludes the document being saved, and excludes the Lead<->Customer pair
    formed by a Customer converted from a Lead in either direction - that
    pair legitimately shares the mobile number, whichever side is being
    validated.

    Returns a list of (found_doctype, found_name) tuples, with matches in
    doc's own doctype listed first (the more direct conflict).
    """
    mobile_no = (doc.mobile_no or "").strip()
    if not mobile_no:
        return []

    lead_filters = {"mobile_no": mobile_no}
    if doc.doctype == "Lead" and not doc.is_new():
        lead_filters["name"] = ["!=", doc.name]
    elif doc.doctype == "Customer" and doc.lead_name:
        lead_filters["name"] = ["!=", doc.lead_name]

    customer_matches = frappe.get_all(
        "Customer", filters={"mobile_no": mobile_no}, fields=["name", "lead_name"]
    )
    if doc.doctype == "Lead":
        customer_matches = [c for c in customer_matches if c.lead_name != doc.name]
    elif doc.doctype == "Customer" and not doc.is_new():
        customer_matches = [c for c in customer_matches if c.name != doc.name]

    duplicate_leads = [
        ("Lead", name) for name in frappe.get_all("Lead", filters=lead_filters, pluck="name")
    ]
    duplicate_customers = [("Customer", c.name) for c in customer_matches]

    # List duplicates within the same doctype first - that is the more direct conflict.
    if doc.doctype == "Customer":
        return duplicate_customers + duplicate_leads
    return duplicate_leads + duplicate_customers


def validate_unique_mobile_no(doc):
    """Throw, linking to every existing document, if doc.mobile_no is
    already used by another Lead or Customer.

    Only runs when Mobile No is new or was just changed on this save - a
    document that already had a duplicate number saved before this check
    existed can still be edited normally without touching Mobile No.
    """
    if not doc.is_new() and not doc.has_value_changed("mobile_no"):
        return

    duplicates = find_duplicate_mobile_no_documents(doc)
    if not duplicates:
        return

    shown, remaining = duplicates[:MAX_DUPLICATES_SHOWN], duplicates[MAX_DUPLICATES_SHOWN:]
    links = [
        get_link_to_form(found_doctype, found_name, label=f"{_(found_doctype)} {found_name}")
        for found_doctype, found_name in shown
    ]
    if remaining:
        links.append(_("and {0} more").format(len(remaining)))

    frappe.throw(
        _("Mobile No {0} is already used in: {1}").format(frappe.bold(doc.mobile_no), ", ".join(links)),
        title=_("Duplicate Mobile No"),
    )
