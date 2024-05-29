import requests

# Define the URL and headers for the first GET request
url_get = "https://smooth-hounds-build.loca.lt/gen?drmId="
headers_get = {
    "User-Agent": "testing"
}

# Send the GET request
response_get = requests.get(url_get, headers=headers_get)

# Parse the JSON response and extract values
if response_get.status_code == 200:
    data = response_get.json()
    id_value = data.get("clientId")
    token_value = data.get("requestToken")
else:
    print(f"Error: GET request failed with status code {response_get.status_code}")
    id_value = None
    token_value = None

# Define the URL and headers for the POST request
url_post = "https://employees-api.dailypay.com/v1/users/password_reset_request_email"
headers_post = {
    "Host": "employees-api.dailypay.com",
    "Accept": "application/json, text/plain, */*",
    "x-correlation-id": "FF7886E9-7151-4681-ACD2-D3B4D1CA5DB9",
    "crossdomain": "true",
    "Accept-Language": "en-IN,en-GB;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "x-castle-client-id": id_value,
    "x-app-bundle": "com.DailyPay.DailyPay",
    "x-app-version": "11.4.12",
    "x-castle-request-token": token_value,
    "User-Agent": "testing",
    "Connection": "keep-alive"
}

# Define the payload for the POST request
user_email = "test@gmail.com"  # Replace with the actual user email
payload = {
    "use_jwt": True,
    "password_reset_request": {
        "email": user_email
    }
}

# Send the POST request
response_post = requests.post(url_post, json=payload, headers=headers_post)

# Check the response of the POST request
if response_post.status_code == 200:
    print("Password reset request email sent successfully.")
else:
    print(f"Error: POST request failed with status code {response_post.status_code}")
