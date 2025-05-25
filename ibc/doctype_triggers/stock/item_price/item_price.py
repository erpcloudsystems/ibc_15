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
    website_items = frappe.db.get_list("Website Item", fields={'item_code'})
    for w in website_items:
        if doc.item_code == w.item_code:
            item = frappe.get_doc("Website Item", {'item_code': doc.item_code})
            price_list = frappe.db.get_single_value('Ecs Woocommerce', 'price_list')
            if doc.price_list == price_list:
                if item.woocommerce_id:
                    woocommerce_user_key = frappe.db.get_single_value('Ecs Woocommerce', 'woocommerce_user_key')
                    woocommerce_user_secret = frappe.db.get_single_value('Ecs Woocommerce', 'woocommerce_user_secret')
                    woocommerce_create = frappe.db.get_single_value('Ecs Woocommerce', 'woocommerce_create')
                    system_url = frappe.db.get_single_value('Ecs Woocommerce', 'system_url')

                    sku = item.item_code
                    item_name = item.web_item_name
                    permalink = "https://example.com/product" + item.web_item_name
                    brand = item.brand
                    item_group = item.item_group
                    image = system_url + item.website_image
                    date_created = item.creation
                    description = item.web_long_description
                    short_description = item.description
                    price = doc.price_list_rate
                    category_id = frappe.db.get_value('Item Group', {'name': item.item_group}, 'category_id')
                    if item.published == 1:
                        status = "publish"
                    else:
                        status = "draft"

                    ## Create Data Structure
                    data = {}
                    data["name"] = item_name
                    data["sku"] = sku
                    data["type"] = "simple"
                    data["status"] = status
                    data["regular_price"] = str(price)
                    data["description"] = item.web_long_description
                    data["short_description"] = item.web_long_description
                    data["image"] = image
                    '''
                    images = []
                    images.append({"src": image})
                    data["images"] = images
                    '''
                    # categories = []
                    # categories.append({"id": category_id})
                    # data["categories"] = categories
                    woocommerce_id = item.woocommerce_id
                    frappe.msgprint(json.dumps(data))

                    headeroauth = OAuth1(woocommerce_user_key, woocommerce_user_secret, None, None,
                                        signature_method='HMAC-SHA1')
                    headers = {
                        "content-type": "application/json;charset=utf-8",
                        "Content-Length": "376",
                        "Connection": "keep-alive",
                        "Accept-Encoding":"gzip, deflate, br",
                        "Accept":"*/*",
                        "User-Agent":"PostmanRuntime/7.42.0"
                    }
                    response = requests.post(
                        url=woocommerce_create + str(woocommerce_id),
                        data=json.dumps(data), auth=headeroauth, headers=headers)
                    encode_data = json.dumps(
                        response.json(), ensure_ascii=False).encode("utf8")
                    response = encode_data.decode()
                    frappe.msgprint(response)


@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
