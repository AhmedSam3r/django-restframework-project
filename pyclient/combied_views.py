
import requests
import json


########detail.py######################
def get_api():
    url = "http://127.0.0.1:8000/product/combined-views/1/"

    resp = requests.get(url=url)

    print("DETAIL(SINGLE PRODUCT) RESP= ", resp.text)
    print(resp.status_code)


########list.py######################
def list_api():
    url = "http://127.0.0.1:8000/product/combined-views/"

    resp = requests.get(url=url)

    print("LISTVIEW RESP= ", resp.text)
    print(resp.status_code)


########create.py######################
def create_api():
    url = "http://127.0.0.1:8000/product/combined-views/"

    data = {
        'title': 'v1.1 initial combined view test'
    }
    resp = requests.post(url=url, json=data)

    print("CREATEVIEW RESP= ", resp.text)
    print(resp.status_code)


get_api()
list_api()
# create_api()