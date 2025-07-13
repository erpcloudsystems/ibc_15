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
    # Get Woocommerce settings
    woocommerce_user_key = frappe.db.get_single_value("Ecs Woocommerce", "woocommerce_user_key")
    woocommerce_user_secret = frappe.db.get_single_value("Ecs Woocommerce", "woocommerce_user_secret")
    woocommerce_api_base = frappe.db.get_single_value("Ecs Woocommerce", "woocommerce_create_category")  # base URL, e.g., https://yourstore.com/wp-json/wc/v3/products/categories/

    # Prepare auth and headers
    auth = OAuth1(
        woocommerce_user_key,
        woocommerce_user_secret,
        None,
        None,
        signature_method="HMAC-SHA1",
    )
    headers = {
        "content-type": "application/json;charset=utf-8"
    }

    # Build the category data payload
    data = {"name": doc.name}

    if doc.parent_item_group:
        parent_category = frappe.db.get_value("Item Group", {"name": doc.parent_item_group}, "category_id")
        if parent_category:
            data["parent"] = parent_category

    # Step 1: If no category_id, check if the category exists on WooCommerce
    if not doc.category_id:
        # Search existing categories by name
        search_url = f"{woocommerce_api_base}?search={doc.name}"
        response = requests.get(search_url, auth=auth, headers=headers)

        if response.status_code == 200:
            existing_categories = response.json()
            if existing_categories:
                # Category found → use its ID
                existing_category_id = existing_categories[0]["id"]
                doc.category_id = existing_category_id
                doc.save()
                return
            else:
                # Step 2: If not found → create a new category
                create_response = requests.post(
                    url=woocommerce_api_base,
                    data=json.dumps(data),
                    auth=auth,
                    headers=headers,
                )
                if create_response.status_code in [200, 201]:
                    returned_data = create_response.json()
                    doc.category_id = returned_data.get("id")
                    doc.save()
                    return
                else:
                    frappe.throw(f"Failed to create category: {create_response.text}")
        else:
            frappe.throw(f"Failed to search for category: {response.text}")
    
    else:
        # If category_id already exists, optionally update the category (if needed)
        update_url = woocommerce_api_base + str(doc.category_id)
        update_response = requests.post(
            url=update_url,
            data=json.dumps(data),
            auth=auth,
            headers=headers,
        )
        frappe.msgprint(f"Category {doc.category_id} updated: {update_response.content}")


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