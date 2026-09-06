from __future__ import unicode_literals
import frappe
from frappe.contacts.doctype.contact.contact import get_default_contact


def sync_customer_mobile_no(customer, mobile_no):
    """Push a mobile number to a Customer's primary Contact, and to Customer.mobile_no.

    Existing contacts are updated with direct db writes (not doc.save()) so that
    unrelated legacy data issues on old Contact records (e.g. more than one row
    already flagged as primary phone) can't block saving the calling document.
    """
    if not customer or not mobile_no:
        return

    mobile_no = mobile_no.strip()
    contact_name = get_default_contact("Customer", customer)

    if contact_name:
        frappe.db.set_value(
            "Contact Phone",
            {"parent": contact_name, "parenttype": "Contact"},
            "is_primary_mobile_no",
            0,
        )
        phone_row = frappe.db.get_value(
            "Contact Phone",
            {"parent": contact_name, "parenttype": "Contact", "phone": mobile_no},
        )
        if phone_row:
            frappe.db.set_value("Contact Phone", phone_row, "is_primary_mobile_no", 1)
        else:
            new_row = frappe.get_doc(
                {
                    "doctype": "Contact Phone",
                    "parent": contact_name,
                    "parenttype": "Contact",
                    "parentfield": "phone_nos",
                    "phone": mobile_no,
                    "is_primary_mobile_no": 1,
                }
            )
            new_row.db_insert()
        frappe.db.set_value("Contact", contact_name, "mobile_no", mobile_no)
    else:
        contact = frappe.new_doc("Contact")
        contact.first_name = frappe.db.get_value("Customer", customer, "customer_name") or customer
        contact.append("links", {"link_doctype": "Customer", "link_name": customer})
        contact.append("phone_nos", {"phone": mobile_no, "is_primary_mobile_no": 1})
        contact.flags.ignore_mandatory = True
        contact.insert(ignore_permissions=True)
        contact_name = contact.name

    primary_contact = frappe.db.get_value("Customer", customer, "customer_primary_contact")
    if not primary_contact:
        frappe.db.set_value("Customer", customer, "customer_primary_contact", contact_name)
        primary_contact = contact_name

    if primary_contact == contact_name:
        # Customer.mobile_no is itself fetched from customer_primary_contact.mobile_no,
        # but that only recomputes on a full document save - set it directly here since
        # this contact was updated with raw db writes above.
        frappe.db.set_value("Customer", customer, "mobile_no", mobile_no)
