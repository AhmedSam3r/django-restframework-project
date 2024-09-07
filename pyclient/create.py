
import requests
import json

url = "http://127.0.0.1:8000/product/1/"

resp = requests.get(url=url)

print("text RESP= ", resp.text)
print(resp.status_code)

url = "http://127.0.0.1:8000/product/create/"

data = {
    'title': 'v1.3 create.py file test'
}
resp = requests.post(url=url, json=data)

print("text RESP= ", resp.text)
print(resp.status_code)
