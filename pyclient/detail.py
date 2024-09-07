import requests
import json

url = "http://127.0.0.1:8000/product/1/"

resp = requests.get(url=url)

print("text RESP= ", resp.text)
print(resp.status_code)
