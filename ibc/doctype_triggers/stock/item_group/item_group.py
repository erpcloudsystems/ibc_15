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
    pass


@frappe.whitelist()
def onload(doc, method=None):
    pass


@frappe.whitelist()
def before_validate(doc, method=None):
    pass


@frappe.whitelist()
def validate(doc, method=None):
    import frappe, json, requests
    from requests_oauthlib import OAuth1

    # Get WooCommerce credentials
    woocommerce_user_key = frappe.db.get_single_value("Ecs Woocommerce", "woocommerce_user_key")
    woocommerce_user_secret = frappe.db.get_single_value("Ecs Woocommerce", "woocommerce_user_secret")
    woocommerce_api_base = frappe.db.get_single_value("Ecs Woocommerce", "woocommerce_create_category").rstrip("/")
    woocommerce_create_category = frappe.db.get_single_value(
        "Ecs Woocommerce", "woocommerce_create_category"
    )

    # Auth and headers
    auth = OAuth1(
        woocommerce_user_key,
        woocommerce_user_secret,
        signature_method="HMAC-SHA1"
    )
    headers = {
        "content-type": "application/json;charset=utf-8",
        "Content-Length": "376",
        "Connection": "keep-alive",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept":"*/*",
        "User-Agent":"PostmanRuntime/7.42.0"
    }

    # Data to send
    data = {"name": doc.name}
    if doc.custom_publish_on_website:
        try:
            if doc.parent_item_group:
                parent_category = frappe.db.get_value("Item Group", {"name": doc.parent_item_group}, "category_id")
                if parent_category:
                    data["parent"] = parent_category

            # If no category_id, first search
            if not doc.category_id:
                search_url = f"{woocommerce_api_base}?search={doc.name}"
                response = requests.get(search_url, auth=auth, headers=headers, timeout=10)

                if response.status_code == 200:
                    existing = response.json()
                    if existing:
                        doc.category_id = existing[0]["id"]
                    else:
                        create_response = requests.post(
                            url=woocommerce_api_base,
                            json=data,
                            auth=auth,
                            headers=headers,
                            timeout=10,
                        )
                        if create_response.status_code in [200, 201]:
                            returned_data = create_response.json()
                            doc.category_id = returned_data.get("id")
                        else:
                            frappe.throw(f"Failed to create category: {create_response.text}")
                else:
                    if doc.parent_item_group:
                        parent_category = frappe.db.get_value(
                            "Item Group", {"name": doc.parent_item_group}, "category_id"
                        )
                        if parent_category:
                            data["parent"] = parent_category

                    # OAuth1 authentication
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
                        "Connection": "keep-alive",
                        "Accept-Encoding":"gzip, deflate, br",
                        "Accept":"*/*",
                        "User-Agent":"PostmanRuntime/7.42.0"
                    }

                    # Step 1: Check if category already exists in WooCommerce
                    check_response = requests.get(
                        url=woocommerce_create_category,
                        params={"search": doc.name},
                        auth=headeroauth,
                        headers=headers,
                        timeout=10,
                    )

                    if check_response.ok:
                        categories = check_response.json()
                        if categories:  # found existing category
                            existing_category = categories[0]
                            doc.category_id = existing_category["id"]
                            frappe.msgprint(f"Category already exists in WooCommerce (ID: {doc.category_id})")
                            return

                    # Step 2: Create category if not found
                    response = requests.post(
                        url=woocommerce_create_category,
                        data=json.dumps(data),
                        auth=headeroauth,
                        headers=headers,
                        timeout=10,
                    )

                    if not response.ok:
                        try:
                            error = response.json()
                            # If category already exists, set the existing ID
                            if error.get("code") == "term_exists":
                                doc.category_id = error["data"]["resource_id"]
                                frappe.msgprint(f"Category already exists in WooCommerce (ID: {doc.category_id})")
                                return
                        except Exception:
                            frappe.throw(f"Failed to create category in WooCommerce: {response.text}")
                        frappe.throw(f"Failed to create category in WooCommerce: {response.text}")
                    returned_data = response.json()
                    doc.category_id = returned_data["id"]
                    frappe.msgprint(f"New category created in WooCommerce (ID: {doc.category_id})")
            else:
                update_url = f"{woocommerce_api_base}/{doc.category_id}"
                update_response = requests.post(
                    url=update_url,
                    json=data,
                    auth=auth,
                    headers=headers,
                    timeout=10,
                )
                frappe.msgprint(f"Category updated: {update_response.content}")
        except requests.exceptions.Timeout:
            frappe.throw(_("Request timed out while connecting to WooCommerce. Please try again later."))
        except requests.exceptions.RequestException as e:
            frappe.throw(_(f"WooCommerce API error: {str(e)}"))


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
    if doc.custom_publish_on_website:
        try:
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
                "Connection": "keep-alive",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept":"*/*",
                "User-Agent":"PostmanRuntime/7.42.0"
            }

            response = requests.post(
                url=woocommerce_create_category + str(category_id),
                data=json.dumps(data),
                auth=headeroauth,
                headers=headers,
                timeout=10,
            )
            frappe.msgprint(f"Category updated: {response}")
        except requests.exceptions.Timeout:
            frappe.throw(_("Request timed out while connecting to WooCommerce. Please try again later."))
        except requests.exceptions.RequestException as e:
            frappe.throw(_(f"WooCommerce API error: {str(e)}"))