import requests
from getpass import getpass
import json

def recursively_list_products(headers):
    resp = json.loads(get_product(headers))
    print('--------resp--------')
    print(resp["results"])    
    next_url = resp.get('next', None)
    print("next url =",next_url)
    while next_url is not None:
        resp = json.loads(requests.get(url=next_url, headers=headers).content)
        print("recusively calling next url")
        print(resp["results"][0])    

        next_url = resp.get('next', None)


def auth():
    url = "http://127.0.0.1:8000/api/auth/"
    # password = getpass()
    data = {
        'username': 'staff',
        'password': '123456_aa'
    }
    print('creds === ', data)
    resp = requests.post(url=url, json=data)
    return resp


def get_product(headers=None):
    url = "http://127.0.0.1:8000/product/list-or-create/"
    resp = requests.get(url=url, headers=headers)
    # print("text RESP= ", resp.text)
    print(resp.status_code)
    return resp.content

def create_product():
    url = "http://127.0.0.1:8000/product/list-or-create/"
    data = {
        'title': 'v1.3 create.py file test'
    }
    resp = requests.post(url=url, json=data)
    print("text RESP= ", resp.text)
    print(resp.status_code)


resp = None
resp = auth()
if resp and resp.status_code == 200:
    print("---SUCCESS AUTH---")
    token = resp.json().get('token')
    headers = {"Authorization": f"Bearer {token}"} # instead of 'Token'
    print(token)
    print('----calling product recursively------')
    recursively_list_products(headers)


# get_product()
'''
Response of product list after pagination

{
    "count":31,
    "next":"http://127.0.0.1:8000/product/list-or-create/?limit=5&offset=5",
    "previous":null,
    "results":[
        {"owner":{"username":"admin","id":1},
                "username":"admin","edit_url":"http://127.0.0.1:8000/product/1/update/","url":"http://127.0.0.1:8000/product/1/","pk":1,"title":"one updated v1.4 mixins","content":"this is the amazing one product","price":"1.44","sale_price":"1.15","get_discount":"122","my_discount":"122"}
        ,{"owner":{"username":"admin","id":1},"username":"admin","edit_url":"http://127.0.0.1:8000/product/2/update/","url":"http://127.0.0.1:8000/product/2/","pk":2,"title":"two","content":"two two two two","price":"1.00","sale_price":"0.80","get_discount":"122","my_discount":"122"},
        {"owner":{"username":"admin","id":1},"username":"admin","edit_url":"http://127.0.0.1:8000/product/4/update/","url":"http://127.0.0.1:8000/product/4/","pk":4,"title":"four added","content":null,"price":"9.99","sale_price":"7.99","get_discount":"122","my_discount":"122"},
        {"owner":{"username":"admin","id":1},"username":"admin","edit_url":"http://127.0.0.1:8000/product/7/update/","url":"http://127.0.0.1:8000/product/7/","pk":7,"title":"TestingCreateAPIview","content":"createapi view","price":"0.00","sale_price":"0.00","get_discount":"122","my_discount":"122"},
        {"owner":{"username":"admin","id":1},"username":"admin","edit_url":"http://127.0.0.1:8000/product/8/update/","url":"http://127.0.0.1:8000/product/8/","pk":8,"title":"create.py file test","content":null,"price":"9.99","sale_price":"7.99","get_discount":"122","my_discount":"122"}
    ]
}
'''
