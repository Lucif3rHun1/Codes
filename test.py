import re
import tls_client
import time

def usercloud(url):
  retry_delay = 1
  match = re.search(r'https://userscloud.com/([a-zA-Z0-9]+)', url)
  file_id = match.group(1)
  post_url = f"https://userscloud.com/{file_id}"
  payload = {
    'op': 'download2',
    'id': file_id,
    'rand': '',
    'referer': '',
    'method_free': '',
    'method_premium': '',
    'down_script': 1,
  }

  while True:
      try:
        session = tls_client.Session(
            client_identifier="chrome112",
            random_tls_extension_order=True
        )
        response = session.post(post_url, data=payload, allow_redirects=False)
        if 'Location' in response.headers:
            download_link = response.headers['Location']
            return download_link
            break  # Successful response, exit the loop
        else:
            print("Failed to retrieve the download link.")
    
      except tls_client.exceptions.TLSClientExeption as e:
          time.sleep(retry_delay)

print(usercloud("https://userscloud.com/d3vwex7s107m"))