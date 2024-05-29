import tls_client
import re
import random
import time
session = tls_client.Session(

    client_identifier="chrome112",

    random_tls_extension_order=True

)
url = "https://dood.so/e/va8hmhoy0zkyff3lgydowoyoqbhl8vaf"
headers = {
    "Host": url,
    "User-Agent": "Mozilla/5.0 (Windows Mankind 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

source = session.get(url,headers=headers,allow_redirects=True)
print(source.text)
pattern1 = r"'/pass_md5/([^/']+)"
pass_md5_match = re.search(pattern1, source.text)
if pass_md5_match:
    pass_md5_value = pass_md5_match.group(1)
    print("pass_md5 value:", pass_md5_value)
else:
    print("No pass_md5 value found.")
pattern2 = r"\?token=([^&]+)"
token_match = re.search(pattern2, source.text)
if token_match:
    token = token_match.group(1)
    print("token value:", token)
else:
    print("No token value found.")

get_url = "https://dood.so/pass_md5/" + pass_md5_value


headers = {
    "Host": url,
    "User-Agent": "Mozilla/5.0 (Windows Mankind 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "X-Requested-With": "XMLHttpRequest",
    "DNT": "1",
    "Connection": "keep-alive",
    "Referer": "<ADDRESS>"
}

source = session.get(get_url,headers=headers,allow_redirects=True)
print(source.text)

# Define the characters for the random string
characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

# Define the length of the random string
length = 10

# Generate a random string
random_string = ''.join(random.choice(characters) for _ in range(length))

# Construct the token with the random string and timestamp
token = random_string + "?token="+token_match+"&expiry=" + str(int(time.time()))

# Assign the DownloadLink variable
DownloadLink = source.text + token



print("Download Link:", DownloadLink)
