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

# request lastest orders from WooCommerce API 
request1 = wcapi.get("orders", params={"per_page": 100, "timeout": 30})
#request2 = wcapi.get("orders", params={"page":2 ,"per_page": 100 ,"timeout": 30})
#request3 = wcapi.get("orders", params={"page":3 ,"per_page": 100 ,"timeout": 30})

requests = [request1]#,request2,request3]

products = wcapi.get("products", params={"per_page": 100})

customer_info = []
product = 'l'
product_id = 2502
# there has to be a better way to do this
# this only runs once a day so I doubt there is much need to improve it
for r in requests:
    for i in range(len(r.json())):
        # Not sure if there is a speed improvement here, idea is to save memory by not creating extra list when we don't need to
        for j in range(len(r.json()[i]['line_items'])):
            if (r.json()[i]['line_items'][j]['product_id'] == product_id):
                relevant_data = [i+1]
                relevant_data.append(r.json()[i]['date_created'])
                relevant_data.append(r.json()[i]['billing']['first_name'] + " " + r.json()[i]['billing']['last_name'])
                relevant_data.append(r.json()[i]['billing']['email'])
                customer_info.append(relevant_data)



    #if (len(r.json()[i]['line_items']) > 1):
    #    for j in range(len(r.json()[i]['line_items'])):
    #      order_items = ""
    #      order_items += r.json()[i]['line_items'][j]['name']
    #      relevant_data.append(order_items)
    #else: relevant_data.append(r.json()[i]['line_items'][0]['name'])

    
with open("student_list_for_product_id_"+str(product_id)+ ".csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(customer_info)
send_email.sendtheemail(["brian.oconnell@thetuitioncentre.ie","conrad@thetuitioncentre.ie"],"student_list_for_product_id_"+str(product_id)+ ".csv", "Student list for Biology ","")