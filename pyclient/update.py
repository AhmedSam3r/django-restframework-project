
import requests
import json

url = "http://127.0.0.1:8000/product/1/update/"

data = {
    'title': 'one updated v1.1',
    'price': 1.11
}
resp = requests.put(url=url, json=data)

print("text RESP= ", resp.text)
print(resp.status_code)
