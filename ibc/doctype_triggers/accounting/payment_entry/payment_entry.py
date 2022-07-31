from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def before_insert(doc, method=None):
    pass
@frappe.whitelist()
def after_insert(doc, method=None):
    pass
@frappe.whitelist()
def onload(doc, method=None):
    pass
@frappe.whitelist()
def before_validate(doc, method=None):
    pass
@frappe.whitelist()
def validate(doc, method=None):
    pass
@frappe.whitelist()
def on_submit(doc, method=None):
    accounts = [
        {
            "doctype": "Journal Entry Account",
            "account": "ايرادات الصيانه - IBC",
            "credit": doc.paid_amount,
            "debit": 0,
            "credit_in_account_currency": doc.paid_amount,
            "user_remark": doc.name,
            "cost_center": "فرع الصيانه -Maintenance - IBC"
        },
        {
            "doctype": "Journal Entry Account",
            "party_type": "Customer",
            "party": doc.party,
            "party_name": doc.party_name,
            "account": doc.paid_from,
            "credit": 0,
            "debit": doc.paid_amount,
            "debit_in_account_currency": doc.paid_amount,
            "user_remark": doc.name
        }
    ]

    if doc.mode_of_payment == "Maintenance":
        jv_doc = frappe.get_doc({
            "doctype": "Journal Entry",
            "posting_date": doc.posting_date,
            "voucher_type": "Journal Entry",
            "company": "IBC",
            "reference_doctype": "Payment Entry",
            "reference_link": doc.name,
            "accounts": accounts,

        })

        jv_doc.insert(ignore_permissions=True)
        jv_doc.submit()
        frappe.msgprint("  تم إنشاء قيد رقم " + jv_doc.name)

@frappe.whitelist()
def on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
