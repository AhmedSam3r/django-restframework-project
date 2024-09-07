
import requests
import json


########detail.py######################
def get_api(product_id):
    url = f"http://127.0.0.1:8000/product/mixin-list/{product_id}/"

    resp = requests.get(url=url)
    res = json.loads(resp.content,)
    print("DETAIL(SINGLE PRODUCT) RESP= ", json.dumps(res, indent=4))
    print(resp.status_code)


########list.py######################
def list_api():
    url = "http://127.0.0.1:8000/product/mixin-list/"

    resp = requests.get(url=url)

    res = json.loads(resp.content,)
    print("LISTVIEW RESP= ", json.dumps(res, indent=4))

    print(resp.status_code)


########create.py######################
def create_api():
    url = "http://127.0.0.1:8000/product/mixin-list/"

    data = {
        'title': 'v1 test perform create in the CreatemixinView'
    }
    resp = requests.post(url=url, json=data)

    print("CREATEVIEW RESP= ", resp.text)
    print(resp.status_code)


def delete_api(product_id):
    # product_id = int(input('enter product id: '))
    url = f"http://127.0.0.1:8000/product/mixin-list/{product_id}/"

    resp = requests.delete(url=url)

    print("text RESP= ", resp.text)
    print(resp.status_code)


def update_api(product_id):
    url = f"http://127.0.0.1:8000/product/mixin-list/{product_id}/"

    data = {
        'title': 'one updated v1.4 mixins',
        'price': 1.44
    }
    resp = requests.put(url=url, json=data)

    print("text RESP= ", resp.text)
    print(resp.status_code)


# list_api()
# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
# get_api(4)
print("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
create_api()
# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
# update_api(1) # 
# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
# delete_api(3) # status code 204 resource has been modified successfully