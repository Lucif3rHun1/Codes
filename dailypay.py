import requests
from bs4 import BeautifulSoup
import threading
# Proxy configuration
proxies = {
    'http': 'http://salem1-zone-resi-region-us:man120@b825788e670315ba.na.pyproxy.io:16666',
    'https': 'http://salem1-zone-resi-region-us:man120@b825788e670315ba.na.pyproxy.io:16666',
}

# Headers configuration
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
headers = {
        'Host': 'app.dailypay.com',
        'User-Agent': ua,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://app.dailypay.com/login',
        'Origin': 'https://app.dailypay.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'trailers'
}

# Session to maintain cookies
session = requests.Session()

def perform_requests():
    token = None

    # First GET request with timeout
    try:
        response1 = session.get("http://students-crm.gl.at.ply.gg:35931/castle?ua=Mozilla/5.0%20(Windows%20NT%2010.0;%20Win64;%20x64;%20rv:120.0)%20Gecko/20100101%20Firefox/120.0", headers=headers, timeout=5)
        token = response1.json().get('token')
        print("Token:", token)
    except Exception as e:
        print("Error in first request:", e)
        # Continue even if the first request fails

    # Second GET request with timeout
    try:
        response2 = session.get("https://app.dailypay.com/forgot_password", 
                                proxies=proxies, headers=headers, timeout=10)
        soup = BeautifulSoup(response2.text, 'html.parser')
        csrf = soup.find('meta', {'name': 'csrf-token'})['content']
        print("CSRF Token:", csrf)
    except Exception as e:
        print("Error in second request:", e)
        return  # Break the script if the second request fails

    # POST request with timeout
    if token and csrf:
        try:
            post_data = {
                'authenticity_token': csrf,
                'forgot_password_email_form[email]': 'test@gmail.com',
                'commit': 'Send Password Reset',
                'castle_request_token': token
            }
            response3 = session.post("https://app.dailypay.com/forgot_password_email", 
                                     data=post_data, proxies=proxies, headers=headers, timeout=10)
            print("Response from POST:", response3.text)
        except Exception as e:
            print("Error in POST request:", e)

perform_requests()
def threaded_request(count):
    threads = []
    for i in range(count):
        t = threading.Thread(target=perform_requests)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

# Example usage
threaded_request(5) 