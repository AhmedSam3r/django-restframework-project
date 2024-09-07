
import requests
import json

product_id = int(input('enter product id: '))
url = f"http://127.0.0.1:8000/product/{product_id}/delete/"

resp = requests.delete(url=url)

print("text RESP= ", resp.text)
print(resp.status_code)
