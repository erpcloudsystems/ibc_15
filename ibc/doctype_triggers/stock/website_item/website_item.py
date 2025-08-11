from __future__ import unicode_literals
import frappe
from frappe import _
import json
import ast
import requests
from requests_oauthlib import OAuth1


@frappe.whitelist()
def before_insert(doc, method=None):
    pass


@frappe.whitelist()
def after_insert(doc, method=None):
    if not doc.website_image:
        frappe.throw(" Please Insert An Image For The Item ")
    # Get Single Values from Ecs Woocommerce seetings page
    price_list = frappe.db.get_single_value("Ecs Woocommerce", "price_list")
    woocommerce_user_key = frappe.db.get_single_value(
        "Ecs Woocommerce", "woocommerce_user_key"
    )
    woocommerce_user_secret = frappe.db.get_single_value(
        "Ecs Woocommerce", "woocommerce_user_secret"
    )
    woocommerce_create = frappe.db.get_single_value(
        "Ecs Woocommerce", "woocommerce_create"
    )
    system_url = frappe.db.get_single_value("Ecs Woocommerce", "system_url")

    # Get Values From Website Item and Item
    sku = doc.item_code
    item1 = frappe.get_doc("Item", doc.item_code)
    if item1.item_name_ar:
        doc.item_name_ar = item1.item_name_ar
    if item1.discription_ar:
        doc.discription_ar = item1.discription_ar
    doc.web_long_description = item1.description
    doc.short_description = item1.description

    doc.save()
    item_name = doc.web_item_name
    # permalink = "https://example.com/product" + doc.web_item_name
    image = system_url + doc.website_image
    price = frappe.db.get_value(
        "Item Price", {"item_code": sku,
                       "price_list": price_list}, ["price_list_rate"]
    )
    category_id = frappe.db.get_value(
        "Item Group", doc.item_group, "category_id")
    if not category_id:
        frappe.throw(" Item Group " + doc.item_group +
                     " Has No WooCommerce ID ")

    # Create Data Structure
    data = {}
    data["name"] = item_name
    data["sku"] = sku
    data["type"] = "simple"
    data["regular_price"] = str(price)
    data["description"] = doc.web_long_description
    data["descs ar"] = doc.web_long_description
    data["short_description"] = doc.web_long_description
    data["image"] = image

    images = []
    images.append({"src": image})
    data["images"] = images

    categories = []
    categories.append({"id": category_id})
    if frappe.db.exists(
        "Website Item Group", {"parent": doc.name}, "item_group"
    ):
        items_groups = frappe.db.get_all(
            "Website Item Group",
            {"parent": doc.name},
            "item_group",

        )
        for item_group in items_groups:
            category_ids = frappe.db.get_value(
                "Item Group", item_group["item_group"], "category_id"
            )

        categories.append({"id": category_ids})
    data["categories"] = categories
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
        url=woocommerce_create, data=json.dumps(data), auth=headeroauth, headers=headers
    )
    frappe.msgprint(response.content)
    returned_data = json.loads(response.content)
    doc.woocommerce_id = returned_data["id"]
    if doc.item_name_ar or doc.discription_ar:
        # normalize the base URL (no trailing slash)
        custom_api_url = "https://vti.erf.mybluehost.me/website_af84c5e9/send/api/update-product.php"


        payload = {
            "token": "s3cr3tM1ddl3w4r3_T0k3n_2025_XyZ",
            "id": sku,
            "name": doc.item_name_ar or "",
            "desc": doc.discription_ar or "",
        }

        try:
            headers={           
                    "Content-Type": "application/json",
                    "Connection": "keep-alive",
                    "Accept":"*/*",
                    "User-Agent":"PostmanRuntime/7.42.0",
                    "Accept-Encoding":"gzip, deflate, br"
                }
            # send as form-encoded POST
            api_response = requests.post(
                custom_api_url,
                data=json.dumps(payload),
                headers=headers
            )

            frappe.msgprint(f"Arabic API response (status {api_response.status_code}):\n{api_response}")
            frappe.msgprint(f"Payload sent: {payload}")

        except Exception:
            frappe.log_error(frappe.get_traceback(), "Arabic Product Update API Error")
            frappe.msgprint("Failed to send Arabic fields to external API.")

    doc.save()


@frappe.whitelist()
def onload(doc, method=None):
    pass


@frappe.whitelist()
def before_validate(doc, method=None):
    pass


import requests
import json
from requests_oauthlib import OAuth1
import frappe

@frappe.whitelist()
def validate(doc, method=None):
    # item1 = frappe.get_doc("Item", doc.item_code)
    # if item1.item_name_ar:
    #     doc.item_name_ar = item1.item_name_ar
    # if item1.discription_ar:
    #     doc.discription_ar = item1.discription_ar
    #     frappe.msgprint(str(doc.discription_ar))
    if doc.woocommerce_id:
        if not doc.website_image:
            frappe.throw("Please Insert An Image For The Item")

        # Get Single Values from Ecs Woocommerce settings page
        price_list = frappe.db.get_single_value("Ecs Woocommerce", "price_list")
        woocommerce_user_key = frappe.db.get_single_value("Ecs Woocommerce", "woocommerce_user_key")
        woocommerce_user_secret = frappe.db.get_single_value("Ecs Woocommerce", "woocommerce_user_secret")
        woocommerce_create = frappe.db.get_single_value("Ecs Woocommerce", "woocommerce_create")
        system_url = frappe.db.get_single_value("Ecs Woocommerce", "system_url")

        # Get Values From Website Item and Item
        sku = doc.item_code
        item_name = doc.web_item_name
        image = system_url + doc.website_image
        price = frappe.db.get_value(
            "Item Price",
            {"item_code": sku, "price_list": price_list},
            ["price_list_rate"],
        )
        category_id = frappe.db.get_value(
            "Item Group", doc.item_group, "category_id")
        if not category_id:
            frappe.throw(f"Item Group {doc.item_group} Has No WooCommerce ID")

        # Set status based on published flag
        status = "publish" if doc.published == 1 else "draft"

        # Create Data Structure for WooCommerce API
        data = {
            "name": item_name,
            "sku": sku,
            "type": "simple",
            "status": status,
            "regular_price": str(price or 0),
            "description": doc.web_long_description or "",
            "short_description": doc.short_description or "",
            "images": [{"src": image}]
        }

        # Add categories
        categories = [{"id": category_id}]
        if frappe.db.exists("Website Item Group", {"parent": doc.name}, "item_group"):
            items_groups = frappe.db.get_all(
                "Website Item Group",
                {"parent": doc.name},
                "item_group"
            )
            for item_group in items_groups:
                category_ids = frappe.db.get_value(
                    "Item Group",
                    item_group["item_group"],
                    "category_id"
                )
                if category_ids:
                    categories.append({"id": category_ids})
        # data["categories"] = categories

        # WooCommerce API Request
        woocommerce_id = doc.woocommerce_id
        headeroauth = OAuth1(
            woocommerce_user_key,
            woocommerce_user_secret,
            None,
            None,
            signature_method="HMAC-SHA1"
        )
        headers = {
            "Content-Type": "application/json;charset=utf-8",
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "*/*",
            "User-Agent": "PostmanRuntime/7.42.0"
        }
        try:
            response = requests.put(
                url=f"{woocommerce_create}{woocommerce_id}",
                data=json.dumps(data, ensure_ascii=False),
                auth=headeroauth,
                headers=headers,
                verify=False  # Bypass SSL for testing
            )
            response_data = response.json()
            frappe.msgprint(f"WooCommerce API response (status {response.status_code}):\n{json.dumps(response_data, ensure_ascii=False)}")
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "WooCommerce API Error")
            frappe.msgprint(f"Failed to update WooCommerce product: {str(e)}")

        # Arabic API Request
        if doc.item_name_ar or doc.discription_ar:
            custom_api_url = "https://vti.erf.mybluehost.me/website_af84c5e9/api/update-product.php"

            params = {
                "token": "s3cr3tM1ddl3w4r3_T0k3n_2025_XyZ",  # exact token
                "id": doc.woocommerce_id,
                "name": doc.item_name_ar or "",
                "desc": doc.discription_ar or "",
                "short_desc": doc.discription_ar or ""
            }

            try:
                response = requests.post(
                    url=custom_api_url,
                    params=params,  # query string params
                    data="",        # empty POST body
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Connection": "keep-alive",
                        "Accept": "*/*",
                        "User-Agent": "PostmanRuntime/7.42.0",
                        "Accept-Encoding": "gzip, deflate, br"
                    }
                )

                response_text = response.content.decode("utf-8", errors="ignore").strip()

                if response.status_code != 200:
                    frappe.msgprint("❌ Arabic product update failed.")
                    frappe.msgprint(f"Status: {response.status_code}")
                    frappe.msgprint(f"Response:\n{response_text}")
                else:
                    frappe.msgprint("✅ Arabic product updated successfully.")
                    frappe.msgprint(response_text)

            except Exception as e:
                frappe.log_error(frappe.get_traceback(), "Arabic Product Update API Error")
                frappe.msgprint("❌ Failed to send Arabic fields to external API.")
@frappe.whitelist()
def before_save(doc, method=None):
    pass


@frappe.whitelist()
def on_update(doc, method=None):
    pass
