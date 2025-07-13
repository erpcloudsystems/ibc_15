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


import frappe
import requests
from requests_oauthlib import OAuth1
import json
import urllib.parse

@frappe.whitelist()
def validate(doc, method=None):
    # Get WooCommerce settings
    woocommerce_user_key = frappe.db.get_single_value("Ecs Woocommerce", "woocommerce_user_key")
    woocommerce_user_secret = frappe.db.get_single_value("Ecs Woocommerce", "woocommerce_user_secret")
    woocommerce_api_base = frappe.db.get_single_value("Ecs Woocommerce", "woocommerce_create_category")

    # Ensure the base URL is correct (no trailing slash)
    if woocommerce_api_base.endswith("/"):
        woocommerce_api_base = woocommerce_api_base.rstrip("/")

    # Prepare auth
    auth = OAuth1(
        client_key=woocommerce_user_key,
        client_secret=woocommerce_user_secret,
        signature_method="HMAC-SHA1",
    )

    # Simplified headers
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # Build the category data payload
    data = {"name": doc.name}

    if doc.parent_item_group:
        parent_category = frappe.db.get_value("Item Group", {"name": doc.parent_item_group}, "category_id")
        if parent_category:
            data["parent"] = parent_category

    # Step 1: If no category_id, check if the category exists on WooCommerce
    if not doc.category_id:
        # URL-encode the search term
        encoded_name = urllib.parse.quote(doc.name)
        search_url = f"{woocommerce_api_base}?search={encoded_name}"
        
        # Log the request for debugging
        frappe.log_error(f"Sending GET request to: {search_url}", "WooCommerce Category Search")

        try:
            response = requests.get(search_url, auth=auth, headers=headers)
            response.raise_for_status()  # Raise an exception for 4xx/5xx errors
            existing_categories = response.json()

            if existing_categories:
                # Category found → use its ID
                existing_category_id = existing_categories[0]["id"]
                doc.category_id = existing_category_id
                # doc.save()
                frappe.msgprint(f"Category found: {doc.name} (ID: {existing_category_id})")
            else:
                # Step 2: If not found → create a new category
                frappe.log_error(f"Creating new category: {json.dumps(data)}", "WooCommerce Category Creation")
                create_response = requests.post(
                    url=woocommerce_api_base,
                    data=json.dumps(data),
                    auth=auth,
                    headers=headers,
                )
                create_response.raise_for_status()  # Raise an exception for 4xx/5xx errors
                returned_data = create_response.json()
                doc.category_id = returned_data.get("id")
                # doc.save()
                frappe.msgprint(f"Category created: {doc.name} (ID: {doc.category_id})")
                
        except requests.exceptions.RequestException as e:
            frappe.log_error(f"API request failed: {str(e)}\nResponse: {response.text}", "WooCommerce API Error")
            frappe.throw(f"Failed to process category: {str(e)}")
    else:
        # If category_id exists, update the category
        update_url = f"{woocommerce_api_base}/{doc.category_id}"
        frappe.log_error(f"Updating category: {update_url} with data: {json.dumps(data)}", "WooCommerce Category Update")
        try:
            update_response = requests.put(  # Use PUT for updates instead of POST
                url=update_url,
                data=json.dumps(data),
                auth=auth,
                headers=headers,
            )
            update_response.raise_for_status()
            frappe.msgprint(f"Category {doc.category_id} updated successfully")
        except requests.exceptions.RequestException as e:
            frappe.log_error(f"Update failed: {str(e)}\nResponse: {update_response.text}", "WooCommerce API Error")
            frappe.throw(f"Failed to update category: {str(e)}")

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