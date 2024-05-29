import tls_client
import re
import random
import string
import time
from bs4 import BeautifulSoup
import html

session = tls_client.Session(
        client_identifier="chrome112",
        random_tls_extension_order=True
    )
url = "https://dood.yt/e/gluh9xpgetuc"
url = url.replace('/d/', '/e/')
host = re.match(r'(https?://[^/]+)(/.*)', url)
host = host.group(1)
Host = re.search(r'https://([^/]+)', url)
Host = Host.group(1)
headers = {
    "Host": Host,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Pragma": "no-cache",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.8"
}
headers2 = {
        "Host": Host,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0",
        "Accept": "*/*",
        "Accept-Language": "en-GB en; q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Requested-With": "XMLHttpRequest",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": url,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "TE": "trailers",
        "Cookie": "referer="
    }
response = session.get(url,headers=headers,allow_redirects=True).text
soup = BeautifulSoup(response, 'html.parser')
title_text = soup.title.string
decoded_title = html.unescape(title_text)
cleaned_title = decoded_title.replace(" - DoodStream", "")
print(cleaned_title)
match = re.search(r"/pass_md5/([^']+)'", response)
get_url = match.group(1)
token_match = re.search(r"token=([^&]+)", response)
token_match = token_match.group(1)
get_url = f"{host}/pass_md5/{get_url}"
print(get_url)
response = session.get(get_url,headers=headers2,allow_redirects=False)
print(response.text)
def make_play():
    token=token_match
    characters = string.ascii_letters + string.digits
    a = ''.join(random.choice(characters) for _ in range(10))
    timestamp = str(int(time.time() * 1000))  # Convert current time to milliseconds and format as a string
    return f"{a}?token={token}&expiry={timestamp}"
durl=response.text+make_play()
print(durl)
