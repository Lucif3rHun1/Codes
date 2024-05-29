import requests
from concurrent.futures import ThreadPoolExecutor
import json

def fetch_token(user_agent):
    url = "http://45.92.1.127:3003/reese84"
    payload = {
        "proxy": "brightdata.vital-proxies.com:22225:lum-customer-vitalkWfNPUHL-zone-residential-country-us:gySQwWvt",
        "userAgent": user_agent,
        "url": "https://epsf.ticketmaster.com/eps-d?d=www.ticketmaster.com"
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response_json = response.json()
        token = response_json.get('token', '')
        return token
    except Exception as e:
        print(f"Error fetching token: {e}")
        return None

def make_request_with_fetched_token(user_agent, proxy):
    token = fetch_token(user_agent)  # Fetch a new token for each request
    if not token:
        print("Failed to retrieve token, skipping this request.")
        return

    url = "https://identity.ticketmaster.com/sign-in?integratorId=prd1741.iccp&placementId=mytmlogin&redirectUri=https%3A%2F%2Fwww.ticketmaster.com%2F"
    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Referer": "https://www.ticketmaster.com.au/",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-User": "?1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Cookie": f"reese84={token}"
    }
    proxies = {
        "http": proxy,
        "https": proxy,
    }
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        print(f"Request made with new token, status code: {response.status_code}")
    except Exception as e:
        print(f"Error making request with new token: {e}")

def main(proxy, user_agent, num_requests=100):
    with ThreadPoolExecutor(max_workers=10) as executor:
        for _ in range(num_requests):
            executor.submit(make_request_with_fetched_token, user_agent, proxy)

if __name__ == "__main__":
    proxy = "http://lum-customer-vitalkWfNPUHL-zone-residential-country-us:gySQwWvt@brightdata.vital-proxies.com:22225"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    main(proxy, user_agent, 100)
