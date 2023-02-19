from __future__ import unicode_literals
import frappe
from frappe import _
import datetime
from frappe.utils import getdate
from frappe.utils import add_to_date


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

    get_checkin = frappe.db.sql(f"""
                                select distinct `tabEmployee Checkin`.time, `tabEmployee Checkin`.log_type,`tabEmployee Checkin`.shift
                                from `tabEmployee Checkin`
                                where `tabEmployee Checkin`.employee = '{doc.employee}'
                                and `tabEmployee Checkin`.log_type = 'IN'
                                order by `tabEmployee Checkin`.time desc
                                """,as_dict = 1)

    for chechin in get_checkin:
        pp = frappe.get_last_doc('Payroll Policy', filters={"shift_type": 'test'})

        for late in pp.late_table:
            
            d = (datetime.datetime.min+late.from_time).time()
            d2 = (datetime.datetime.min+late.to_time).time()

            if chechin.time.date() == getdate(doc.attendance_date):
                if chechin.time.time() >= d and chechin.time.time() <= d2:
                    extra_salary = frappe.get_doc({
                        'doctype': 'Extra Salary',
                        'company': 'IBC',
                        'employee' : doc.employee,
                        'salary_component' : late.salary_component,
                        'amount' : late.deduct_value_hours,
                        'payroll_date' : doc.attendance_date,
                        'overwrite_salary_structure_amount' : 1,
                        'deduct_full_tax_on_selected_payroll_date' : 0,
                        'posted' : 0

                    })
                    extra_salary.submit()
                    doc.log_type = 'Present'
                    doc.submit()
                    frappe.msgprint("Extra Salary has been created")
                # elif  chechin.time.time() >= datetime.time(9, 00) and chechin.time.time() <= datetime.time(9, 15):
                #     doc.status = 'Present'


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
