from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import get_link_to_form

MAX_DUPLICATES_SHOWN = 5


def find_duplicate_mobile_no_documents(doc):
    """Find every other Lead/Customer already using doc.mobile_no.

    Excludes the document being saved, and - for a Customer that was
    converted from a Lead - excludes that same originating Lead, since it
    legitimately shares the mobile number.

    Returns a list of (found_doctype, found_name) tuples, with matches in
    doc's own doctype listed first (the more direct conflict).
    """
    mobile_no = (doc.mobile_no or "").strip()
    if not mobile_no:
        return []

    lead_filters = {"mobile_no": mobile_no}
    customer_filters = {"mobile_no": mobile_no}

    if doc.doctype == "Lead":
        if not doc.is_new():
            lead_filters["name"] = ["!=", doc.name]
    elif doc.doctype == "Customer":
        if not doc.is_new():
            customer_filters["name"] = ["!=", doc.name]
        if doc.lead_name:
            lead_filters["name"] = ["!=", doc.lead_name]

    duplicate_leads = [
        ("Lead", name) for name in frappe.get_all("Lead", filters=lead_filters, pluck="name")
    ]
    duplicate_customers = [
        ("Customer", name) for name in frappe.get_all("Customer", filters=customer_filters, pluck="name")
    ]

    # List duplicates within the same doctype first - that is the more direct conflict.
    if doc.doctype == "Customer":
        return duplicate_customers + duplicate_leads
    return duplicate_leads + duplicate_customers


def validate_unique_mobile_no(doc):
    """Throw, linking to every existing document, if doc.mobile_no is
    already used by another Lead or Customer."""
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
