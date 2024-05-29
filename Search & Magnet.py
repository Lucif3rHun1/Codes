import requests
import re
from bs4 import BeautifulSoup
from itertools import zip_longest
import os
import time
import json
import tls_client
import random

CACHE_FILE = 'cache1.json'  # Define the cache file path
magnets_file_path = 'magnets.txt'


def load_cache():
    """Load the cache from the JSON file."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as cache_file:
            return json.load(cache_file)
    return {}

def clear_cache():
    global cache
    cache = {}

def save_cache():
    """Save the cache to the JSON file."""
    with open(CACHE_FILE, 'w') as cache_file:
        json.dump(cache, cache_file, indent=4)


def extract_title(title):
    if '[' not in title and ']' not in title:
        return title
    title = title.replace('[', '').replace(']', '').strip()
    words_to_check = ['hail']
    unwanted_chars = [',', '!', '&', '?', '…', '(', ')']
    pattern = r'\([^)]*\)'

    def replace_unwanted_chars(match):
        match = match.group(0).replace('-', ' ')
        match = re.sub(
            f'[{"".join(map(re.escape, unwanted_chars))}]',
            '',
            match,
        )
        return match

    if [word for word in words_to_check if word in title]:
        title = re.sub(pattern, '', title)
    else:
        if '/' in title and ',' in title and (date := re.findall(r'\d{2}\.\d{2}\.\d{4}', title)):
            title = title.split(',', 1)[0]
            title = f'{title} {date[0]}'
        title = re.sub(pattern, replace_unwanted_chars, title)

    return title


def search_torrents(parsed_title):
    if parsed_title in cache:
        cache_entry = cache[parsed_title]
        if 'search_response' in cache_entry and 'torrent_links' in cache_entry:
            search_response = cache_entry['search_response']
            torrent_links = cache_entry['torrent_links']
        else:
            # The cache structure is invalid; reinitialize it
            del cache[parsed_title]
            return search_torrents(parsed_title, cache)
    else:
        search_url = f"https://www.1377x.to/search/{parsed_title}/1/"
        while True:
            try:
                search_response = requests.get(search_url)
                if search_response.status_code == 200:
                    break
            except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
                print(
                    f"An error occurred: {e}. Retrying title search for {parsed_title} in 1337x...")
                time.sleep(5)

        # Initialize the cache entry
        cache[parsed_title] = {
            'search_response': search_response,
            'torrent_links': []
        }

    search_soup = BeautifulSoup(search_response.text, 'html.parser')
    if torrent_links := search_soup.select('a[href^="/torrent/"]'):
        # Update the cache with the latest torrent_links
        cache[parsed_title]['torrent_links'] = torrent_links

    return search_response


def get_user_choice(max_choice):
    while True:
        choice_input = input(
            "Enter the number of the torrent you want to download, 'm' to enter title manually, or press enter or '0' to skip: "
        )
        if choice_input in ["", "0", "m"]:
            return choice_input
        try:
            choice = int(choice_input)
            if 1 <= choice <= max_choice:
                return choice
            else:
                print(
                    f"Invalid choice. Please enter a number between 1 and {max_choice}.")
        except ValueError:
            print("Invalid input. Please enter a number or 'm'.")

def write_torrent(parsed_title):
    if parsed_title not in cache or 'torrent_entries' not in cache[parsed_title]:
        print(f"No torrent entries found for title: {parsed_title}")
        return

    torrent_entries = cache[parsed_title]['torrent_entries']
    if not torrent_entries:
        return

    torrent_links = cache[parsed_title]['torrent_links']
    torrent_names = [entry['name'] for entry in torrent_entries]
    seeds = [entry['seeds'] for entry in torrent_entries]
    sizes = [entry['size'] for entry in torrent_entries]
    print("{:<4} {:<70} {:<10} {:<10}".format(
        "No.", "Name", "Seeds", "Size"))
    for i, (name, seed, size) in enumerate(zip_longest(torrent_names, seeds, sizes, fillvalue='N/A'), start=1):
        print("{:<4} {:<70} {:<10} {:<10}".format(i, name, seed, size))

    user_choice = get_user_choice(len(torrent_names))

    if user_choice in ["", "0"]:
        return
    elif user_choice == "m":
        manual_title = input("Enter the title manually: ")
        return process_title(manual_title)
    else:
        selected_torrent_index = int(user_choice) - 1

        if 0 <= selected_torrent_index < len(torrent_entries):
            torrent_url = f"https://www.1377x.to{torrent_links[selected_torrent_index]}"
            torrent_entries.pop(selected_torrent_index)
            torrent_links.pop(selected_torrent_index)
            cache[parsed_title]['torrent_entries'] = torrent_entries
            cache[parsed_title]['torrent_links'] = torrent_links

            while True:
                try:
                    torrent_response = requests.get(torrent_url)
                    if torrent_response.status_code == 200:
                        break
                except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
                    print(
                        f"An error occurred: {e}. Retrying torrent page link for {torrent_url} in 1337x...")
                    time.sleep(5)

            torrent_soup = BeautifulSoup(
                torrent_response.text, 'html.parser')
            if magnet_link := torrent_soup.select_one(
                'a[href^="magnet:"]'
            ):
                with open(magnets_file_path, 'a') as magnets_file:
                    magnets_file.write(magnet_link["href"] + "\n")
                print(
                    f"Saved magnet link for torrent {selected_torrent_index + 1}.")
            else:
                print("Failed to fetch magnet link for this torrent.")

        write_torrent(parsed_title)



def process_title(title):
    parsed_title = extract_title(title)
    print(f"Parsed Title: {parsed_title}")

    if parsed_title not in cache and not update_data(parsed_title):
        print(f"No torrents found for this title: {parsed_title}")
        user_choice = input(
            "Enter 'm' to manually enter a title, '0' to skip, or press Enter: ")
        if user_choice == "m":
            manual_title = input("Enter the title manually: ")
            return process_title(manual_title)
        elif user_choice in ["", "0"]:
            return

    write_torrent(parsed_title)

def update_data(parsed_title):
    search_response = search_torrents(parsed_title)
    search_soup = BeautifulSoup(search_response.text, 'html.parser')
    links = search_soup.select('a[href^="/torrent/"]')
    if links:
        torrent_links = []
        for tl in links:
            torrent_links.append(tl['href'])
        search_html = str(search_soup)
        torrent_names = re.findall(
            r'<a href="/torrent[^>]+>(.*?)<', search_html)
        seeds = re.findall(
            r'(?<=<td class="coll-2 seeds">)\d+(?=<)', search_html)
        sizes = [match[0] for match in re.findall(
            r'<td class="coll-4 size mob-\w+">([\d.]+\s?(MB|GB)|\d+\s?(MB|GB))<\/td>', search_html)]
        torrent_entries = []
        for name, size, seed in zip(torrent_names, sizes, seeds):
            entry = {'name': name,
                     'size': size,
                     'seeds': seed}
            torrent_entries.append(entry)

        cache[parsed_title] = {'title': parsed_title,
                               'search_response': search_response.text,
                               'torrent_entries': torrent_entries,
                               'torrent_links': torrent_links}
        return True
    else:
        print(f"No links found for title: {parsed_title}")
        return False

def process_link(link, links):
    print(f"Processing link: {link}")

    # Clear the cache when moving to the next URL
    clear_cache()

    session = tls_client.Session(
        client_identifier="chrome112",
        random_tls_extension_order=True
    )
    response = session.get(link)
    if response.status_code != 200:
        print(f"Failed to fetch the page: {link}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    title_element = soup.select_one('h1.g1-mega')

    if not title_element:
        print("No title element found on the page.")
        return

    title = title_element.get_text().strip()

    # Skip torrents even if titles are available
    if "torrent" in title.lower():
        print("Skipped the link as it appears to be a torrent.")
        return

    process_title(title)

    # Remove the processed link from the 'links' list
    links.remove(link)

def main():
    with open('links.txt', 'r') as file:
        links = [link.strip() for link in file.readlines()]

    if not links:
        print("No links found in the file.")
        return

    num_links_to_process = len(links)

    magnets_saved = 0

    # Load the cache at the beginning
    cache = load_cache()

    for progress in range(num_links_to_process):
        if not links:
            break

        link = links[0]  # Process the first link in the list
        print(f"Progress: {progress + 1:02}/{num_links_to_process:02}")
        print(
            f"Remaining links to process: {num_links_to_process - progress:02}")
        # Process the link using the process_link function
        process_link(link, links)

        # Remove the processed link from the file
        with open('links.txt', 'w') as file:
            file.writelines('\n'.join(links))

    # Save the cache at the end
    if cache:
        save_cache()

    print("All links processed.")

if __name__ == "__main__":
    main()
