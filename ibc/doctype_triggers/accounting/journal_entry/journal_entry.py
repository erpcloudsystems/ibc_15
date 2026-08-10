from __future__ import unicode_literals
import frappe
from frappe import _


def before_insert(doc, method=None):
    pass

def after_insert(doc, method=None):
    pass

def onload(doc, method=None):
    pass

def before_validate(doc, method=None):
    pass

def validate(doc, method=None):
    if doc.user_remark:
        doc.title = doc.user_remark
    else:
        doc.title = doc.name
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
    pass
