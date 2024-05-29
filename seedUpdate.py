import requests
from bs4 import BeautifulSoup
import re
import time
import asyncio
from aiogram import Bot
from datetime import datetime, timedelta

# Replace these with your own Telegram Bot API token and chat_id
telegram_token = "6348937556:AAGkj-mocLdNBSP2S6BF_tPumnBhmcNBO_s"
telegram_chat_id = "5016416878"

# Initialize the Telegram Bot
bot = Bot(token=telegram_token)

# Initialize variables to store scraped data
combined_data = ""
scenetime_data = ""
hdfans_data = ""
pussytorrents_data = ""

# Function to send or edit a message in Telegram
async def send_or_edit_telegram_message(text):
    try:
        current_time = datetime.now() # Add +5:30 GMT
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        if not send_or_edit_telegram_message.message_id:
            message = await bot.send_message(chat_id=telegram_chat_id, text=f"{text}\n\nLast Updated: {formatted_time}")
            send_or_edit_telegram_message.message_id = message.message_id
        else:
            await bot.edit_message_text(chat_id=telegram_chat_id, message_id=send_or_edit_telegram_message.message_id, text=f"{text}\n\nLast Updated: {formatted_time}")
    except Exception as e:
        print(f"Error sending/editing message: {str(e)}")

send_or_edit_telegram_message.message_id = None

# Function to scrape HDFans using BeautifulSoup
async def HDFans():
    global hdfans_data

    # Add your cookies here
    cookies = {
        'c_lang_folder': 'en',
        'c_secure_ssl': 'eWVhaA%3D%3D',
        'amp_6e403e': 'Zebkeb_OxuUevOmWJ5S9Y8...1hc33jj7j.1hc33m6m1.0.0.0',
        'c_secure_uid': 'NDU3MzE%3D',
        'c_secure_pass': 'b8a3f79ed995d457e852fc821debeeda',
        'c_secure_tracker_ssl': 'eWVhaA%3D%3D',
        'c_secure_login': 'bm9wZQ%3D%3D',
    }

    try:
        # Make the request with cookies
        response = requests.get("https://hdfans.org/index.php", headers={"Cookie": "; ".join([f"{key}={value}" for key, value in cookies.items()])})

        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the elements containing the values
            ratio_element = soup.find('font', class_='color_ratio')
            uploaded_element = soup.find('font', class_='color_uploaded')
            downloaded_element = soup.find('font', class_='color_downloaded')

            if ratio_element and uploaded_element and downloaded_element:
                # Extract the values
                ratio = ratio_element.find_next_sibling(string=True).strip()
                uploaded = uploaded_element.find_next_sibling(string=True).strip()
                downloaded = downloaded_element.find_next_sibling(string=True).strip()

                # Update HDFans data
                hdfans_data = f"HDFans: Ratio: {ratio}, Uploaded: {uploaded}, Downloaded: {downloaded}"
            else:
                hdfans_data = "Failed to extract data from HDFans. Elements not found."
        else:
            hdfans_data = f"Failed to fetch HDFans. Status code: {response.status_code}"
    except requests.exceptions.RequestException as req_err:
        hdfans_data = f"Request error while scraping HDFans: {req_err}"
    except AttributeError as attr_err:
        hdfans_data = f"Attribute error while scraping HDFans: {attr_err}"
    except Exception as e:
        hdfans_data = f"Error while scraping HDFans: {str(e)}"

# Function to scrape Scenetime using BeautifulSoup
async def Scenetime():
    global scenetime_data

    # Add your cookies here
    cookies = {
        'cf_clearance': 'aUU7LjkoOE4lC.zB.k6V5rJz0THIm0h7V2mkbDHaHTY-1696495389-0-1-49d475bd.959a7a18.1ed52a5d-150.0.0',
        'uid': '473419',
        'pass': '3c70679994a8fec5f2052bbd0b8ac43e',
        'PHPSESSID': '68dpcg7h4fb1c9ffrko6udjc0l',
        'amp_6e403e': 'Zebkeb_OxuUevOmWJ5S9Y8...1hc27giik.1hc295ltq.0.0.0',
    }

    try:
        # Make the request with cookies
        response = requests.get("https://www.scenetime.com/index.php", headers={"Cookie": "; ".join([f"{key}={value}" for key, value in cookies.items()])})

        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the element containing the data
            data_element = soup.find('div', class_='FLl')

            if data_element:
                # Extract the text content
                data_text = data_element.get_text(strip=True)

                # Extract values using leftstring and rightstring
                ratio = data_text.split("(", 1)[0]  # Left part before "("
                ratio_value = data_text.split("(", 1)[1].split(")", 1)[0]  # Value inside "(" and ")"
                uploads = data_text.split("Up:")[1].split("DL:")[0].strip()
                downloads = data_text.split("DL:")[1].split("GB")[0].strip()

                # Update Scenetime data
                scenetime_data = f"SceneTime: Ratio: {ratio_value}, Uploaded: {uploads}, Downloaded: {downloads} GB"
            else:
                scenetime_data = "Failed to extract values from Scenetime. Element not found."
        else:
            scenetime_data = f"Failed to fetch Scenetime. Status code: {response.status_code}"
    except requests.exceptions.RequestException as req_err:
        scenetime_data = f"Request error while scraping Scenetime: {req_err}"
    except Exception as e:
        scenetime_data = f"Error while scraping Scenetime: {str(e)}"

# Function to scrape PussyTorrents using BeautifulSoup
async def PussyTorrents():
    global pussytorrents_data

    # Add your cookies here
    cookies = {
        's__chb': '1',
        's__ljs': '1',
        'lastBrowse1': '1696429159',
        'lastBrowse2': '1696431586',
        'amp_6e403e': 'Zebkeb_OxuUevOmWJ5S9Y8...1hbtm70qe.1hbtm70qe.0.0.0',
        'PHPSESSID': 'v5jk095irdptlma06rja0ph548',
        'ptuid': '3141664',
        'ptpass': 'd935b59f96fec7b92dd03a497b456fb83f968950',
    }

    try:
        # Make the request with cookies
        response = requests.get("https://pussytorrents.org/", headers={"Cookie": "; ".join([f"{key}={value}" for key, value in cookies.items()])})

        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the element containing the data
            data_element = soup.find('div', class_='span8')

            if data_element:
                # Extract the text containing the ratio, uploaded, and downloaded
                data_text = data_element.get_text()

                # Use regex to extract the ratio, uploaded, and downloaded
                ratio_match = re.search(r'Ratio:\s*([\d.]+)', data_text)
                uploaded_match = re.search(r'UL:\s*([\d.]+\s*\w+)', data_text)
                downloaded_match = re.search(r'DL:\s*([\d.]+\s*\w+)', data_text)

                if ratio_match and uploaded_match and downloaded_match:
                    # Extract the values from the regex matches
                    ratio = ratio_match.group(1)
                    uploaded = uploaded_match.group(1)
                    downloaded = downloaded_match.group(1)

                    # Update PussyTorrents data
                    pussytorrents_data = f"PussyTorrents: Ratio: {ratio}, Uploaded: {uploaded}, Downloaded: {downloaded}"
                else:
                    pussytorrents_data = "Failed to extract data from PussyTorrents. Data not found."
            else:
                pussytorrents_data = "Failed to extract data from PussyTorrents. Element not found."
        else:
            pussytorrents_data = f"Failed to fetch PussyTorrents. Status code: {response.status_code}"
    except requests.exceptions.RequestException as req_err:
        pussytorrents_data = f"Request error while scraping PussyTorrents: {req_err}"
    except AttributeError as attr_err:
        pussytorrents_data = f"Attribute error while scraping PussyTorrents: {attr_err}"
    except Exception as e:
        pussytorrents_data = f"Error while scraping PussyTorrents: {str(e)}"
# Function to scrape BitSexy using BeautifulSoup
async def BitSexy():
    global bitsexy_data

    # Add your cookies here
    cookies = {
        'PHPSESSID': 'o9us6an6uf9nace9v0se8jms62',
        'tbalpha_uid': '35524',
        'tbalpha_pass': '44de067cc7eeaf7c7eb60d6eb6e549e1',
        'tbalpha_hashv': 'ecf41b4fbf0f26a8c77a50d3cb4f7355',
        'amp_6e403e': 'Zebkeb_OxuUevOmWJ5S9Y8...1hc0t3423.1hc0t3423.0.0.0',
    }

    try:
        # Make the request with cookies
        response = requests.get("https://www.bitsexy.org/index.php", headers={"Cookie": "; ".join([f"{key}={value}" for key, value in cookies.items()])})

        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the element containing the data
            data_element = soup.find('div', class_='statusbar')

            if data_element:
                # Extract the text containing the ratio, uploaded, and downloaded
                data_text = data_element.get_text()
                
                data_text = ' '.join(data_text.split())
                # Use regex to extract the ratio, uploaded, and downloaded
                ratio_match = re.search(r'Ratio\s*([\d.]+)', data_text)
                uploaded_match = re.search(r'Uploaded:\s*([\d.]+\s*[\w.]+)', data_text)
                downloaded_match = re.search(r'Downloaded:\s*([\d.]+\s*[\w.]+)', data_text)

                if ratio_match and uploaded_match and downloaded_match:
                    # Extract the values from the regex matches
                    ratio = ratio_match.group(1)
                    uploaded = uploaded_match.group(1)
                    downloaded = downloaded_match.group(1)

                    # Update BitSexy data
                    bitsexy_data = f"BitSexy: Ratio: {ratio}, Uploaded: {uploaded}, Downloaded: {downloaded}"
                else:
                    bitsexy_data = "Failed to extract data from BitSexy. Data not found."
            else:
                bitsexy_data = "Failed to extract data from BitSexy. Element not found."
        else:
            bitsexy_data = f"Failed to fetch BitSexy. Status code: {response.status_code}"
    except requests.exceptions.RequestException as req_err:
        bitsexy_data = f"Request error while scraping BitSexy: {req_err}"
    except AttributeError as attr_err:
        bitsexy_data = f"Attribute error while scraping BitSexy: {attr_err}"
    except Exception as e:
        bitsexy_data = f"Error while scraping BitSexy: {str(e)}"
# Main function to run the scraper and send messages
async def main():
    while True:
        await BitSexy()
        await Scenetime()
        await HDFans()
        await PussyTorrents()
        
    # Combine all data
        combined_data = f"{scenetime_data}\n{hdfans_data}\n{pussytorrents_data}\n{bitsexy_data}"
        print(combined_data)
        # Send or edit the combined data to Telegram
        await send_or_edit_telegram_message(combined_data)

        # Sleep for 30 minutes before refreshing
        await asyncio.sleep(1 * 60)

if __name__ == "__main__":
    asyncio.run(main())
