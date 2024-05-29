import requests
from bs4 import BeautifulSoup
import time
import json
import threading


# Define your Telegram Bot Token and Chat ID
TOKEN = '5078059228:AAGnRXUzVZVeZrW0xPZXzzCEdEuOdBr1lms'
CHAT_ID = '5063769209'

# Define the URLs to monitor
URL1 = 'https://www.bluedart.com/web/guest/trackdartresult?trackFor=0&trackNo=70062174151#SCAN70062174151'
URL2 = 'https://www.bluedart.com/web/guest/trackdartresult?trackFor=0&trackNo=70062174151#SCAN79880131730'

# CSS selectors for location and status for each URL
SELECTORS = {
    URL1: {
        'LOCATION_SELECTOR': '#SCAN70062174151 > div > table > tbody > tr:nth-child(1) > td:nth-child(1)',
        'STATUS_SELECTOR': '#SCAN79880131730 > div > table > tbody > tr:nth-child(1) > td:nth-child(2)',
    },
    URL2: {
        'LOCATION_SELECTOR': '#SCAN70062174151 > div > table > tbody > tr:nth-child(1) > td:nth-child(1)',
        'STATUS_SELECTOR': '#SCAN79880131730 > div > table > tbody > tr:nth-child(1) > td:nth-child(2)',
    },
}

# Function to send a message to the Telegram bot via Telegram API
def send_message_via_api(text):
    api_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {
        'chat_id': CHAT_ID,
        'text': text
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(api_url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        return response.status_code
    except Exception as e:
        print(f"Error sending message via API: {str(e)}")
        return None

# Initialize variables to store the previous values for each URL
previous_values = {url: {'location': None, 'status': None} for url in [URL1, URL2]}

# Function to monitor a URL
def monitor_url(url):
    while True:
        try:
            selectors = SELECTORS[url]
            print(f"Checking URL: {url}")

            # Make an HTTP request to fetch the webpage content
            response = requests.get(url)

            if response.status_code == 200:
                print("Request successful")

                # Parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract location and status elements
                location_element = soup.select_one(selectors['LOCATION_SELECTOR'])
                status_element = soup.select_one(selectors['STATUS_SELECTOR'])

                if location_element is not None and status_element is not None:
                    # Extract inner HTML content
                    new_location = location_element.decode_contents()
                    new_status = status_element.decode_contents()

                    # Get the previous values for this URL
                    previous_location = previous_values[url]['location']
                    previous_status = previous_values[url]['status']

                    # Check if the values have changed
                    if previous_location is not None and previous_status is not None:
                            message = f"URL: {url}\nLocation: {new_location}\nStatus: {new_status}"

                            # Print the parsed values to the console for debugging
                            print(message)

                            # Send the message to Telegram via the Telegram API
                            response_code = send_message_via_api(message)

                            if response_code == 200:
                                print("Message sent successfully")
                            else:
                                print(f"Failed to send message. Response code: {response_code}")

                    # Update the previous values for this URL
                    previous_values[url]['location'] = new_location
                    previous_values[url]['status'] = new_status

                else:
                    # If location or status elements are not found, reset the previous values
                    previous_values[url]['location'] = None
                    previous_values[url]['status'] = None

            # Wait for 10 seconds before the next check for this URL
            time.sleep(10)
            print(f"Waiting for 10 seconds for {url}...")

        except Exception as e:
            print(f"Error: {str(e)}")
            # In case of an error, continue checking after a delay
            time.sleep(10)
            print(f"Waiting for 10 seconds after an error for {url}...")

# Create threads to monitor each URL separately
thread1 = threading.Thread(target=monitor_url, args=(URL1,))
thread2 = threading.Thread(target=monitor_url, args=(URL2,))

# Start the threads
thread1.start()
thread2.start()

# Wait for the threads to finish (in this case, they run indefinitely)
thread1.join()