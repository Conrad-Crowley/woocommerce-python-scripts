from woocommerce import API
import csv
import send_email
import config
import json

wcapi = API(
    url="https://thetuitioncentre.ie",
    consumer_key=config.consumer_key,
    consumer_secret=config.consumer_secret,
    version="wc/v3"
)
# Keys I don't want
# This could possibly be slower that it's compliment (UPDATE: Testing seems to indicate no)
useless_keys = ['parent_id','number','order_key','created_via','version', 'status', 'currency','date_created','date_modified',
"date_modified_gmt",  'discount_total', 'discount_tax', 'shipping_total', 'shipping_tax', 'cart_tax', 
 'total_tax', 'prices_include_tax', 'customer_id', 'customer_ip_address', 'customer_user_agent', 'customer_note', 'shipping', 'payment_method', 'payment_method_title', 'transaction_id', 'date_paid', 'date_paid_gmt', 'date_completed', 'date_completed_gmt', 'cart_hash', 'meta_data', 'tax_lines', 'shipping_lines', 'fee_lines', 'refunds', 'currency_symbol', '_links']


# request lastest orders from WooCommerce API 
r = wcapi.get("orders", params={"per_page": 10, "timeout": 30})
request = r.json()
test_data = request[0]
#request2 = wcapi.get("orders", params={"page":2 ,"per_page": 100 ,"timeout": 30})
#request3 = wcapi.get("orders", params={"page":3 ,"per_page": 100 ,"timeout": 30})
for i in range(len(request)):
    for key in useless_keys:
        try:
            del request[i][key]
        except KeyError:
            pass

keys = request[0].keys()
print(keys)
#with open('people.csv', 'w', newline='')  as output_file:
#    dict_writer = csv.DictWriter(output_file, keys)
#    dict_writer.writeheader()
#    dict_writer.writerows(request)
