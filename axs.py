import requests
import random
import json

def ip():
    return "akamai1-zone-resi-region-us:josueee66@e7418db9296aadc6.na.pyproxy.io:16666"

# cwellman1113@gmail.com:Leeder1113 | Points = 5750
def login():
    url = "http://57.128.134.237:9022/login"
    data = {
        "proxy": ip(),
        "site": "str",
        "acc": "cwellman1113",
        "pwd": "Leeder1113"
    }
    r = requests.post(url=url, json=data)
    print(r.text)
    return r.json()

def get_points(cookie_dict: dict):
    url = "http://57.128.134.237:9022/get_points"
    data = {
        "proxy": ip(),
        "site": "str",
        "cookie": cookie_dict  # No need to json.dumps() here
    }
    print(data)
    r = requests.post(url=url, json=data)
    return r.text

cookie_obj = login()

a = {
    "access_token": cookie_obj["access_token"],
    "id_token": cookie_obj["id_token"]
}

point = get_points(cookie_dict=a)
print(point)
