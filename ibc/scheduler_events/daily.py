from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def daily():
    # Combined brand and item_group updates for each DocType (14 queries -> 7 queries)
    # Added WHERE clause to only update records that differ
    
    # Delivery Note Item
    frappe.db.sql("""
        UPDATE `tabDelivery Note Item` t
        JOIN `tabItem` i ON t.item_code = i.name
        SET t.brand = i.brand, t.item_group = i.item_group
        WHERE t.brand != i.brand OR t.item_group != i.item_group
           OR t.brand IS NULL OR t.item_group IS NULL
    """)
    
    # Purchase Invoice Item
    frappe.db.sql("""
        UPDATE `tabPurchase Invoice Item` t
        JOIN `tabItem` i ON t.item_code = i.name
        SET t.brand = i.brand, t.item_group = i.item_group
        WHERE t.brand != i.brand OR t.item_group != i.item_group
           OR t.brand IS NULL OR t.item_group IS NULL
    """)
    
    # Purchase Order Item
    frappe.db.sql("""
        UPDATE `tabPurchase Order Item` t
        JOIN `tabItem` i ON t.item_code = i.name
        SET t.brand = i.brand, t.item_group = i.item_group
        WHERE t.brand != i.brand OR t.item_group != i.item_group
           OR t.brand IS NULL OR t.item_group IS NULL
    """)
    
    # Purchase Receipt Item
    frappe.db.sql("""
        UPDATE `tabPurchase Receipt Item` t
        JOIN `tabItem` i ON t.item_code = i.name
        SET t.brand = i.brand, t.item_group = i.item_group
        WHERE t.brand != i.brand OR t.item_group != i.item_group
           OR t.brand IS NULL OR t.item_group IS NULL
    """)
    
    # Sales Invoice Item
    frappe.db.sql("""
        UPDATE `tabSales Invoice Item` t
        JOIN `tabItem` i ON t.item_code = i.name
        SET t.brand = i.brand, t.item_group = i.item_group
        WHERE t.brand != i.brand OR t.item_group != i.item_group
           OR t.brand IS NULL OR t.item_group IS NULL
    """)
    
    # Sales Order Item
    frappe.db.sql("""
        UPDATE `tabSales Order Item` t
        JOIN `tabItem` i ON t.item_code = i.name
        SET t.brand = i.brand, t.item_group = i.item_group
        WHERE t.brand != i.brand OR t.item_group != i.item_group
           OR t.brand IS NULL OR t.item_group IS NULL
    """)
    
    # Stock Ledger Entry - only update where NULL or different
    frappe.db.sql("""
        UPDATE `tabStock Ledger Entry` sle
        JOIN `tabItem` i ON sle.item_code = i.name
        SET sle.brand = i.brand, sle.item_group = i.item_group
        WHERE sle.brand IS NULL OR sle.item_group IS NULL
           OR sle.brand != i.brand OR sle.item_group != i.item_group
    """)
    
    frappe.db.commit()
    
    #update_woocommerce()
  
@frappe.whitelist()
def update_woocommerce():
    pass
    ## Get Single Values from Ecs Woocommerce seetings page
    # price_list = frappe.db.get_single_value('Ecs Woocommerce', 'price_list')
    # woocommerce_user_key = frappe.db.get_single_value('Ecs Woocommerce', 'woocommerce_user_key')
    # woocommerce_user_secret = frappe.db.get_single_value('Ecs Woocommerce', 'woocommerce_user_secret')
    # woocommerce_create = frappe.db.get_single_value('Ecs Woocommerce', 'woocommerce_create')
    # system_url = frappe.db.get_single_value('Ecs Woocommerce', 'system_url')

    # ## Get Values From Website Item and Item
    # website_item_list = frappe.db.get_list('Website Item', filters={'published': 1},
    #                                        fields=['name',
    #                                                'item_code',
    #                                                'web_item_name',
    #                                                'woocommerce_id',
    #                                                'brand',
    #                                                'item_group',
    #                                                'website_image',
    #                                                'creation',
    #                                                'published',
    #                                                'web_long_description',
    #                                                'description'
    #                                                ])
    # for x in website_item_list:
    #     sku = x.item_code
    #     item_name = x.web_item_name
    #     permalink = "https://example.com/product" + x.web_item_name
    #     brand = x.brand
    #     item_group = x.item_group
    #     image = system_url + x.website_image
    #     date_created = x.creation
    #     description = x.web_long_description
    #     short_description = x.description
    #     price = frappe.db.get_value('Item Price', {'item_code': sku, 'price_list': price_list}, ['price_list_rate'])
    #     category_id = frappe.db.get_value('Item Group', x.item_group, 'category_id')
    #     if x.published == 1:
    #         status = "publish"
    #     else:
    #         status = "draft"

    #     ## Create Data Structure
    #     data = {}
    #     data["name"] = item_name
    #     data["sku"] = sku
    #     data["type"] = "simple"
    #     data["status"] = status
    #     data["regular_price"] = str(price)
    #     data["description"] = x.web_long_description
    #     data["short_description"] = x.web_long_description
    #     data["image"] = image
    #     '''
    #     images = []
    #     images.append({"src": image})
    #     data["images"] = images
    #     '''
    #     categories = []
    #     categories.append({"id": category_id})
    #     data["categories"] = categories
    #     woocommerce_id = x.woocommerce_id
    #     # frappe.msgprint(json.dumps(data))

    #     headeroauth = OAuth1(woocommerce_user_key, woocommerce_user_secret, None, None,
    #                          signature_method='HMAC-SHA1')
    #     headers = {'content-type': 'application/json;charset=utf-8',
    #                "Content-Length": "376"
    #                }
    #     response = requests.post(
    #         url=woocommerce_create + str(woocommerce_id),
    #         data=json.dumps(data), auth=headeroauth, headers=headers)

