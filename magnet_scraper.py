import requests
import re
import os
from bs4 import BeautifulSoup
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import tls_client

def extract_title(title):
    # Check if the title contains '/'
    slash_index = title.find('/')
    if slash_index != -1:
        # If the title contains '/', extract the part inside [] and till the first comma
        bracket_match = re.search(r'\[(.*?)\]', title)
        if bracket_match:
            parsed_title = bracket_match.group(1).strip()

        first_comma_index = title.find(',')
        if first_comma_index != -1:
            parsed_title += " " + title[slash_index + 1:first_comma_index].strip()
    else:
        # If no '/', parse the whole title removing [] and commas
        parsed_title = re.sub(r'\[.*?\]', '', title).strip()
        parsed_title = parsed_title.replace(',', '')

    return parsed_title

def main():
    # Set the proxy URL
    proxy_url = "http://pr.pyproxy.com:16666:owner111-zone-resi-region-us:owner111"

    # Prompt the user to select a text file
    Tk().withdraw()
    filename = askopenfilename()
    
    # Check if file is selected
    if not filename:
        print("No file selected.")
        return

    # Read the links from the text file
    with open(filename, 'r') as file:
        links = file.readlines()

    # Clean up the links (remove newline characters)
    links = [link.strip() for link in links]

    # Create a tls_client session
    session = tls_client.Session(
        client_identifier="chrome112",
        random_tls_extension_order=True
    )

    # List to store magnet links
    all_magnets = []

    # Iterate through each link
    for link in links:
        try:
            print(f"Processing link: {link}")
            response = session.get(link)

            # Check if the request was successful (status code 200)
            if response.status_code != 200:
                print(f"Request to the link failed with status code {response.status_code}.")
                continue

            response_content = response.text
            soup = BeautifulSoup(response_content, 'html.parser')

            title_element = soup.select_one('h1.g1-mega')
            if title_element:
                title = title_element.get_text().strip()
                print(f"Original title: {title}")

                parsed_title = extract_title(title)
                print(f"Parsed title: {parsed_title}")

                # Make a request to 1377x.to with the modified title using tls_client and the proxy
                search_url = f"https://www.1377x.to/search/{parsed_title}/1/"
                search_response = requests.get(search_url, proxies={'http': proxy_url, 'https': proxy_url})

                # Check if the request was successful (status code 200)
                if search_response.status_code != 200:
                    print(f"Request to 1377x.to failed with status code {search_response.status_code}.")
                    continue

                # Download magnet links
                magnets = []
                search_soup = BeautifulSoup(search_response.text, 'html.parser')
                magnet_links = search_soup.find_all('a', href=True)
                for a in magnet_links:
                    if 'magnet:' in a['href']:
                        magnets.append(a['href'])

                all_magnets.extend(magnets)
            else:
                print("Title element not found on the page.")
        except Exception as e:
            print(f"Error processing link: {link} - {e}")

    # Save magnet links to a file
    with open('magnets.txt', 'w') as f:
        for magnet in all_magnets:
            f.write("%s\n" % magnet)

if __name__ == "__main__":
    main()
