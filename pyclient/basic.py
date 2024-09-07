import requests
import json

url_status = "https://httpbin.org/status/200"

url_anything = "https://httpbin.org/anything"

url_basic = "https://httpbin.org"

url_local = "http://127.0.0.1:8000/api/"
url_local_product = "http://127.0.0.1:8000/api/product/"
url_local_add_product = "http://127.0.0.1:8000/api/product/add/"

# resp = requests.get(url=url_local_product, params={"param_1": 1},
#                      json={'json_key': 'json_value'})
# # print("---RESP---", resp.json())
# print("text RESP= ", resp.text)
# print(resp.status_code)

resp = requests.post(url=url_local_add_product, params={"param_1": 1},
                     json={'json_key': 'json_value', 'title': 'new title', 'price': 'abc'})
# print("---RESP---", resp.json())
print("text RESP= ", resp.text)
print(resp.status_code)

