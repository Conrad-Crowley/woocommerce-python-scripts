from woocommerce import API
import csv
import send_email
import config

wcapi = API(
    url="https://thetuitioncentre.ie",
    consumer_key=config.consumer_key,
    consumer_secret=config.consumer_secret,
    version="wc/v3"
)

# request lastest orders from WooCommerce API 
r = wcapi.get("orders", params={"per_page": 20})

customer_info = []
# there has to be a better way to do this
# this only runs once a day so I doubt there is much need to improve it
for i in range(len(r.json())):
    relevant_data = [i+1]
    relevant_data.append(r.json()[i]['date_paid_gmt'])
    # Not sure if there is a speed improvement here, idea is to save memory by not creating extra list when we don't need to
    if (len(r.json()[i]['line_items']) > 1):
        for j in range(len(r.json()[i]['line_items'])):
          order_items = ""
          order_items += r.json()[i]['line_items'][j]['name']
          relevant_data.append(order_items)
    else: relevant_data.append(r.json()[i]['line_items'][0]['name'])
    relevant_data.append(r.json()[i]['total'])
    relevant_data.append(r.json()[i]['billing']['first_name'] + " " + r.json()[i]['billing']['last_name'])
    relevant_data.append(r.json()[i]['billing']['email'])
    customer_info.append(relevant_data)

with open("recent_orders.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(customer_info)
send_email.sendtheemail(["conrad@thetuitioncentre.ie"],"recent_orders.csv", "Email report with recent orders" ,"Based")