from __future__ import unicode_literals
import frappe
from frappe import _
import json, ast, requests
from requests_oauthlib import OAuth1


@frappe.whitelist()
def before_insert(doc, method=None):
    pass


@frappe.whitelist()
def after_insert(doc, method=None):
    ## Get Single Values from Ecs Woocommerce seetings page
    woocommerce_user_key = frappe.db.get_single_value(
        "Ecs Woocommerce", "woocommerce_user_key"
    )
    woocommerce_user_secret = frappe.db.get_single_value(
        "Ecs Woocommerce", "woocommerce_user_secret"
    )
    woocommerce_create_category = frappe.db.get_single_value(
        "Ecs Woocommerce", "woocommerce_create_category"
    )

    ## Create Data Structure
    data = {}
    data["name"] = doc.name
    if doc.parent_item_group:
        parent_category = frappe.db.get_value(
            "Item Group", {"name": doc.parent_item_group}, "category_id"
        )
        data["parent"] = parent_category

    # frappe.msgprint(json.dumps(data))

    headeroauth = OAuth1(
        woocommerce_user_key,
        woocommerce_user_secret,
        None,
        None,
        signature_method="HMAC-SHA1",
    )
    headers = {
        "content-type": "application/json;charset=utf-8",
        "Content-Length": "376",
    }
    response = requests.post(
        url=woocommerce_create_category,
        data=json.dumps(data),
        auth=headeroauth,
        headers=headers,
    )
    # frappe.msgprint(response.content)
    frappe.msgprint(response.content)

    returned_data = json.loads(response.content)
    
    doc.category_id = returned_data["id"]
    doc.save()
    doc.reload()


@frappe.whitelist()
def onload(doc, method=None):
    pass


@frappe.whitelist()
def before_validate(doc, method=None):
    pass


@frappe.whitelist()
def validate(doc, method=None):
    # Fetch required settings only once
    woocommerce_user_key = frappe.db.get_single_value("Ecs Woocommerce", "woocommerce_user_key")
    woocommerce_user_secret = frappe.db.get_single_value("Ecs Woocommerce", "woocommerce_user_secret")
    woocommerce_create_category = frappe.db.get_single_value("Ecs Woocommerce", "woocommerce_create_category")

    # Prepare category creation data
    data = {"name": doc.name}

    if doc.parent_item_group:
        parent_category = frappe.db.get_value("Item Group", {"name": doc.parent_item_group}, "category_id")
        if parent_category:
            data["parent"] = parent_category

    # Set up OAuth1 and headers
    headeroauth = OAuth1(
        woocommerce_user_key,
        woocommerce_user_secret,
        None,
        None,
        signature_method="HMAC-SHA1",
    )
    headers = {
        "content-type": "application/json;charset=utf-8"
    }

    # If category_id is missing, create a new one
    if not doc.category_id:
        response = requests.post(
            url=woocommerce_create_category,
            data=json.dumps(data),
            auth=headeroauth,
            headers=headers,
        )
        frappe.msgprint(f"Response from WooCommerce: {response.content}")

        if response.status_code == 201:
            returned_data = response.json()
            doc.category_id = returned_data.get("id")
            doc.save()
            doc.reload()
        else:
            frappe.throw(f"Failed to create category: {response.text}")
    else:
        # Optional: update existing category (if needed)
        response = requests.post(
            url=woocommerce_create_category + str(doc.category_id),
            data=json.dumps(data),
            auth=headeroauth,
            headers=headers,
        )
        frappe.msgprint(f"Updated category {doc.category_id}: {response.content}")


@frappe.whitelist()
def before_save(doc, method=None):
    pass


@frappe.whitelist()
def on_update(doc, method=None):
    pass


@frappe.whitelist()
def after_rename(first, name, before_rename, after_rename, bool_arg):
    ## Get Single Values from Ecs Woocommerce seetings page
    woocommerce_user_key = frappe.db.get_single_value(
        "Ecs Woocommerce", "woocommerce_user_key"
    )
    woocommerce_user_secret = frappe.db.get_single_value(
        "Ecs Woocommerce", "woocommerce_user_secret"
    )
    woocommerce_create_category = frappe.db.get_single_value(
        "Ecs Woocommerce", "woocommerce_create_category"
    )
    doc = frappe.get_doc("Item Group", after_rename)
    category_id = doc.category_id
    new_name = doc.name
    ## Create Data Structure
    data = {}
    data["name"] = new_name
    if doc.parent_item_group:
        parent_category = frappe.db.get_value(
            "Item Group", {"name": doc.parent_item_group}, "category_id"
        )
        data["parent"] = parent_category
    # frappe.msgprint(json.dumps(data))

    headeroauth = OAuth1(
        woocommerce_user_key,
        woocommerce_user_secret,
        None,
        None,
        signature_method="HMAC-SHA1",
    )
    headers = {
        "content-type": "application/json;charset=utf-8",
        "Content-Length": "376",
    }
    response = requests.post(
        url=woocommerce_create_category + str(category_id),
        data=json.dumps(data),
        auth=headeroauth,
        headers=headers,
    )