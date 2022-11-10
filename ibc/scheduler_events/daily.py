from __future__ import unicode_literals
import frappe
from frappe import _

frappe.whitelist()
def daily():
    frappe.db.sql(
        """update tabBin inner join tabItem on tabItem.item_code = tabBin.item_code set tabBin.brand = tabItem.brand where tabItem.valuation_rate != 1000000112 """)
    frappe.db.sql(
        """update tabBin join tabItem on tabBin.item_code = tabItem.name set tabBin.item_group = tabItem.item_group""")
    frappe.db.sql(
        """update `tabSales Invoice` join `tabCustomer` set `tabSales Invoice`.c_sales_person = `tabCustomer`.sales_person where `tabSales Invoice`.c_sales_person is null""")
    frappe.db.sql(
        """update `tabSales Order` join `tabCustomer` set `tabSales Order`.c_sales_person = `tabCustomer`.sales_person where `tabSales Order`.c_sales_person is null""")
    frappe.db.sql(
        """update `tabDelivery Note Item` join `tabItem` on `tabDelivery Note Item`.item_code = `tabItem`.name set `tabDelivery Note Item`.brand = `tabItem`.brand""")
    frappe.db.sql(
        """update `tabDelivery Note Item` join `tabItem` on `tabDelivery Note Item`.item_code = `tabItem`.name set `tabDelivery Note Item`.item_group = `tabItem`.item_group""")
    frappe.db.sql(
        """update `tabPurchase Invoice Item` join `tabItem` on `tabPurchase Invoice Item`.item_code = `tabItem`.name set `tabPurchase Invoice Item`.brand = `tabItem`.brand""")
    frappe.db.sql(
        """update `tabPurchase Invoice Item` join `tabItem` on `tabPurchase Invoice Item`.item_code = `tabItem`.name set `tabPurchase Invoice Item`.item_group = `tabItem`.item_group""")
    frappe.db.sql(
        """update `tabPurchase Order Item` join `tabItem` on `tabPurchase Order Item`.item_code = `tabItem`.name set `tabPurchase Order Item`.brand = `tabItem`.brand""")
    frappe.db.sql(
        """update `tabPurchase Order Item` join `tabItem` on `tabPurchase Order Item`.item_code = `tabItem`.name set `tabPurchase Order Item`.item_group = `tabItem`.item_group""")
    frappe.db.sql(
        """update `tabPurchase Receipt Item` join `tabItem` on `tabPurchase Receipt Item`.item_code = `tabItem`.name set `tabPurchase Receipt Item`.brand = `tabItem`.brand""")
    frappe.db.sql(
        """update `tabPurchase Receipt Item` join `tabItem` on `tabPurchase Receipt Item`.item_code = `tabItem`.name set `tabPurchase Receipt Item`.item_group = `tabItem`.item_group""")
    frappe.db.sql(
        """update tabQuotation set tabQuotation.creator = tabQuotation.owner where tabQuotation.creator is null""")
    frappe.db.sql(
        """update `tabSales Invoice Item` join `tabItem` on `tabSales Invoice Item`.item_code = `tabItem`.name set `tabSales Invoice Item`.brand = `tabItem`.brand""")
    frappe.db.sql(
        """update `tabSales Invoice Item` join `tabItem` on `tabSales Invoice Item`.item_code = `tabItem`.name set `tabSales Invoice Item`.item_group = `tabItem`.item_group""")
    frappe.db.sql(
        """update `tabSales Order Item` join `tabItem` on `tabSales Order Item`.item_code = `tabItem`.name set `tabSales Order Item`.brand = `tabItem`.brand""")
    frappe.db.sql(
        """update `tabSales Order Item` join `tabItem` on `tabSales Order Item`.item_code = `tabItem`.name set `tabSales Order Item`.item_group = `tabItem`.item_group""")
    frappe.db.sql(
        """update `tabStock Ledger Entry` inner join tabItem on tabItem.item_code = `tabStock Ledger Entry`.item_code set `tabStock Ledger Entry`.brand = tabItem.brand where `tabStock Ledger Entry`.brand IS NULL""")
    frappe.db.sql(
        """update `tabStock Ledger Entry` join tabItem on `tabStock Ledger Entry`.item_code = tabItem.name set `tabStock Ledger Entry`.item_group = tabItem.item_group""")

    update_woocommerce()

frappe.whitelist()
def update_woocommerce():
    ## Get Single Values from Ecs Woocommerce seetings page
    price_list = frappe.db.get_single_value('Ecs Woocommerce', 'price_list')
    woocommerce_user_key = frappe.db.get_single_value('Ecs Woocommerce', 'woocommerce_user_key')
    woocommerce_user_secret = frappe.db.get_single_value('Ecs Woocommerce', 'woocommerce_user_secret')
    woocommerce_create = frappe.db.get_single_value('Ecs Woocommerce', 'woocommerce_create')
    system_url = frappe.db.get_single_value('Ecs Woocommerce', 'system_url')

    ## Get Values From Website Item and Item
    website_item_list = frappe.db.get_list('Website Item', filters={'published': 1},
                                           fields=['name',
                                                   'item_code',
                                                   'web_item_name',
                                                   'woocommerce_id',
                                                   'brand',
                                                   'item_group',
                                                   'website_image',
                                                   'creation',
                                                   'published',
                                                   'web_long_description',
                                                   'description'
                                                   ])
    for x in website_item_list:
        sku = x.item_code
        item_name = x.web_item_name
        permalink = "https://example.com/product" + x.web_item_name
        brand = x.brand
        item_group = x.item_group
        image = system_url + x.website_image
        date_created = x.creation
        description = x.web_long_description
        short_description = x.description
        price = frappe.db.get_value('Item Price', {'item_code': sku, 'price_list': price_list}, ['price_list_rate'])
        category_id = frappe.db.get_value('Item Group', x.item_group, 'category_id')
        if x.published == 1:
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
        data["description"] = x.web_long_description
        data["short_description"] = x.web_long_description
        data["image"] = image
        '''
        images = []
        images.append({"src": image})
        data["images"] = images
        '''
        categories = []
        categories.append({"id": category_id})
        data["categories"] = categories
        woocommerce_id = x.woocommerce_id
        # frappe.msgprint(json.dumps(data))

        headeroauth = OAuth1(woocommerce_user_key, woocommerce_user_secret, None, None,
                             signature_method='HMAC-SHA1')
        headers = {'content-type': 'application/json;charset=utf-8',
                   "Content-Length": "376"
                   }
        response = requests.post(
            url=woocommerce_create + str(woocommerce_id),
            data=json.dumps(data), auth=headeroauth, headers=headers)

