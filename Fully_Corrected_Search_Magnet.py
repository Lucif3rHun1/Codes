import requests
import re
from bs4 import BeautifulSoup
from tkinter import Tk, filedialog
from itertools import zip_longest
import tls_client
import time
import random

class TorrentScraper:
    def __init__(self, proxy_url):
        self.proxy_url = proxy_url
        self.session = tls_client.Session(
            client_identifier="chrome112",
            random_tls_extension_order=True
        )
    self.search_results_cache = {}
self.saved_titles = set()

def extract_title(self, title):
parsed_title = title.replace('[', '').replace(']', '').strip()
open_paren_index = parsed_title.find('(')
close_paren_index = parsed_title.find(')')

if open_paren_index != -1 and close_paren_index != -1:
text_inside_parentheses = parsed_title[open_paren_index + 1:close_paren_index]
unwanted_chars = [',', '!', '&', '?', '…', '(', ')']
unwanted_chars_space = ['-']

for char in unwanted_chars:
text_inside_parentheses = text_inside_parentheses.replace(char, '')
for char in unwanted_chars_space:
text_inside_parentheses = text_inside_parentheses.replace(char, ' ')

parsed_title = parsed_title[:open_paren_index] + text_inside_parentheses + parsed_title[close_paren_index + 1:]

slash_index = parsed_title.find('/')
if slash_index != -1:
first_comma_index = parsed_title.find(',')
if first_comma_index != -1:
parsed_title = parsed_title[:first_comma_index].strip()
else:
parsed_title = parsed_title[:slash_index].strip()
else:
date_regex = r'\d{2}\.\d{2}\.\d{4}'
if re.match(date_regex, parsed_title):
parsed_title = ""

words = parsed_title.split()
unique_words = []
for word in words:
if word not in unique_words:
unique_words.append(word)
parsed_title = ' '.join(unique_words)

return parsed_title

def search_torrents(self, parsed_title):
if parsed_title in self.search_results_cache:
return self.search_results_cache[parsed_title]

search_url = f"https://www.1377x.to/search/{parsed_title}/1/"

while True:
try:
search_response = requests.get(search_url, proxies={'http': self.proxy_url, 'https': self.proxy_url})
if search_response.status_code == 200:
break
except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
print(f"An error occurred: {e}. Retrying title search for {parsed_title} in 1337x...")
time.sleep(5)

search_soup = BeautifulSoup(search_response.text, 'html.parser')
torrent_links = search_soup.select('a[href^="/torrent/"]')

self.search_results_cache[parsed_title] = (search_response, torrent_links)
return search_response, torrent_links

def get_user_choice(self, max_choice):
while True:
choice_input = input("Enter the number of the torrent you want to download, enter 't' to manually enter a title, or press enter or '0' to skip: ")
if choice_input == "" or choice_input == "0":
return 0
elif choice_input.lower() == "t":
manual_title = input("Enter the manual title: ")
return manual_title
try:
choice = int(choice_input)
if 1 <= choice <= max_choice:
return choice
else:
print(f"Invalid choice. Please enter a number between 1 and {max_choice}.")
except ValueError:
print("Invalid input. Please enter a number or 't' for manual title.")

def process_links(self, links, num_links):
for _ in range(num_links):
link = random.choice(links)
links.remove(link)
print(f"Processing link: {link}")
response = self.session.get(link)
if response.status_code == 200:
response_content = response.text
soup = BeautifulSoup(response_content, 'html.parser')

title_element = soup.select_one('h1.g1-mega')
if title_element:
title = title_element.get_text().strip()
print(f"Original title: {title}")
parsed_title = self.extract_title(title)
print(f"Parsed title: {parsed_title}")

search_response, torrent_links = self.search_torrents(parsed_title)
if search_response is None or not torrent_links:
print("No torrents found for this title.")
continue

search_soup = BeautifulSoup(search_response.text, 'html.parser')
search_html = str(search_soup)
torrent_names = re.findall(r'<a href="/torrent[^>]+>(.*?)<', search_html)
seeds = re.findall(r'(?<=<td class="coll-2 seeds">)\d+(?=<)', search_html)
pattern = r'<td class="coll-4 size mob-\w+">(\d+\.\d+\s?(MB|GB))<\/td>'
sizes = re.findall(pattern, search_html)
sizes = [match[0] for match in sizes]

print("Number of torrent links found:", len(torrent_links))
print("{:<4} {:<70} {:<10} {:<10}".format("No.", "Name", "Seeds", "Size"))
for i, (name, seed, size) in enumerate(zip_longest(torrent_names, seeds, sizes, fillvalue='N/A'), start=1):
print("{:<4} {:<70} {:<10} {:<10}".format(i, name, seed, size))

choice = self.get_user_choice(len(torrent_links))
if choice == 0:
break
elif isinstance(choice, int):
torrent_response = requests.get(f"https://1337x.to{torrent_links[choice-1]['href']}",
proxies={'http': self.proxy_url, 'https': self.proxy_url})
if torrent_response.status_code == 200:
magnet_link = self.extract_magnet_link(torrent_response)
self.save_magnet_link(magnet_link, parsed_title)
self.saved_titles.add(parsed_title)
else:
print(f"Request to the torrent link failed with status code {torrent_response.status_code}. Response content: {torrent_response.text}")
self.delete_magnet_links()
else:  # Manual title
parsed_title = self.extract_title(choice)
if parsed_title in self.search_results_cache:
del self.search_results_cache[parsed_title]  # Remove cached data for manually entered title
continue
else:
print("Title element not found on the page.")
else:
print(f"Request to the link failed with status code {response.status_code}.")

self.remove_duplicate_links(filename)


def remove_duplicate_links(self, filename):
with open(filename, 'r') as file:
lines = file.readlines()

unique_links = list(set([line.strip() for line in lines]))

with open(filename, 'w') as file:
for link in unique_links:
file.write(f"{link}\n")

print("Duplicate links removed and saved.")

def extract_magnet_link(self, torrent_response):
torrent_soup = BeautifulSoup(torrent_response.text, 'html.parser')
magnet_link = torrent_soup.select_one('a[href^="magnet:"]')['href']
print("Found magnet link:", magnet_link)
return magnet_link

def save_magnet_link(self, magnet_link, title):
if title in self.saved_titles:
return  # Avoid counting duplicates

with open('magnets.txt', 'a') as magnets_file:
magnets_file.write(f"{title} - {magnet_link}\n")
print("Saved magnet link for title:", title)

def delete_magnet_links(self):
with open('magnets.txt', 'r') as file:
lines = file.readlines()

with open('magnets.txt', 'w') as file:
for line in lines:
if line.strip() not in self.saved_titles:
file.write(line)

def run(self):
proxy_url = "http://thundergdalcxdb13C-res-ROW:lgurvrrexfvvtp57R@gw.thunderproxies.net:5959"
Tk().withdraw()
filename = filedialog.askopenfilename()

if not filename:
print("No file selected.")
exit()

with open(filename, 'r') as file:
links = file.readlines()

links = list(set([link.strip() for link in links]))

num_links = int(input("Enter the number of links to process: "))
if num_links > len(links):
num_links = len(links)

self.process_links(links, num_links)

if __name__ == "__main__":
scraper = TorrentScraper(proxy_url="http://thundergdalcxdb13C-res-ROW:lgurvrrexfvvtp57R@gw.thunderproxies.net:5959")
scraper.run()