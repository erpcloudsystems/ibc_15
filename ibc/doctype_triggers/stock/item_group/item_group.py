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
        "Connection": "keep-alive",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept":"*/*",
        "User-Agent":"PostmanRuntime/7.42.0"
    }
    response = requests.post(
        url=woocommerce_create_category,
        data=json.dumps(data),
        auth=headeroauth,
        headers=headers,
    )
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
    # pass
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
    if item1.website_ar:
        doc.web_long_description = item1.discription_ar
        doc.short_description = item1.discription_ar
    if not item1.website_ar:
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
    doc.save()


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
    # frappe.msgprint(response.content)

