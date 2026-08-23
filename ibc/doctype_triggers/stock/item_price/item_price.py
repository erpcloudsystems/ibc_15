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
                    image = system_url.rstrip("/") + "/" + item.website_image.lstrip("/")
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
                    data["description"] = item.description
                    data["short_description"] = item.description
                    data["image"] = image
                    '''
                    images = []
                    images.append({"src": image})
                    data["images"] = images
                    '''
                    category_id = frappe.db.get_value("Item Group", item.item_group, "category_id")
                    if not category_id:
                        frappe.throw(" Item Group " + item.item_group + " Has No WooCommerce ID.")

                    categories = []
                    categories.append({"id": category_id})
                    if frappe.db.exists(
                        "Website Item Group", {"parent": item.name}, "item_group"
                    ):
                        items_groups = frappe.db.get_all(
                            "Website Item Group",
                            {"parent": item.name},
                            "item_group",

                        )
                        for item_group in items_groups:
                            category_ids = frappe.db.get_value(
                                "Item Group", item_group["item_group"], "category_id"
                            )

                        categories.append({"id": category_ids})
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
                    # encode_data = json.dumps(
                    #     response.json(), ensure_ascii=False).encode("utf8")
                    # response = encode_data.decode()
                    frappe.msgprint(response.content)
            if item.item_name_ar or item.discription_ar:
                custom_api_url = "https://vti.erf.mybluehost.me/website_af84c5e9/api/update-product.php"

                params = {
                    "token": "s3cr3tM1ddl3w4r3_T0k3n_2025_XyZ",
                    "id": item.woocommerce_id,
                    "name": item.item_name_ar or "",
                    "desc": item.discription_ar or "",
                    "short_desc": item.discription_ar or ""
                }

                try:
                    response = requests.post(
                        url=custom_api_url,
                        params=params,  # query string params
                        data="",        # empty POST body
                        headers={
                            "Content-Type": "application/json",
                            "Connection": "keep-alive",
                            "Accept":"*/*",
                            "User-Agent":"PostmanRuntime/7.42.0",
                            "Accept-Encoding":"gzip, deflate, br",
                            "Cookie": "humans_21909=1"
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
