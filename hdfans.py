import requests
from bs4 import BeautifulSoup
import time
import os
import re
import base64
import json
import logging

# Setup basic logging
logging.basicConfig(filename='hdfans.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def imageHash(session):
    request_url = 'https://hdfans.org/login.php?secret=&sitelanguage=6'
    try:
        request = session.get(request_url)    
    except requests.RequestException as e:
        logging.error(f"Network error while fetching image hash: {e}")
        return None

    pattern = 'imagehash=([A-Za-z0-9]+)&'
    match = re.search(pattern, request.text)
    if match:
        logging.info(f"Image hash found: {match.group(1)}")
        return match.group(1)
    else:
        logging.warning("No image hash found")
        return None

def solve(hash_value):
    solve_url = f'https://hdfans.org/image.php?action=regimage&imagehash={hash_value}&secret='
    try:
        body = requests.get(solve_url)
    except requests.RequestException as e:
        logging.error(f"Network error while fetching CAPTCHA image: {e}")
        return None

    body_encoded = base64.b64encode(body.content).decode('utf-8')
    solver_url = 'https://api.capsolver.com/createTask'
    data = {
        "clientKey": "CAP-7D0544F78315BEF99FAC5B075ED11A55",
        "task": {
            "type": "ImageToTextTask",
            "module": "common",
            "body": body_encoded
        }
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(solver_url, data=json.dumps(data), headers=headers)
        response_data = response.json()
        solution_text = response_data.get('solution', {}).get('text')
        logging.info(f"CAPTCHA solution: {solution_text}")
        return solution_text
    except requests.RequestException as e:
        logging.error(f"Network error while solving CAPTCHA: {e}")
        return None
    except json.JSONDecodeError:
        logging.error("Error decoding JSON from CAPSOLVER")
        return None

def login_and_save_cookies(solution, hash_value):
    session = requests.Session()
    login_url = "https://hdfans.org/takelogin.php"
    payload = {
        'secret': '',
        'username': 'Lucif3rHun1',
        'password': 'LuciferHun_12',
        'two_step_code': '',
        'imagestring': solution,
        'imagehash': hash_value
    }

    try:
        response = session.post(login_url, data=payload)
        if response.ok:
            with open('cookies.txt', 'w') as file:
                file.write(str(session.cookies.get_dict()))
            logging.info("Login successful, cookies saved.")
        else:
            logging.error("Login failed")
            return None
    except requests.RequestException as e:
        logging.error(f"Network error during login: {e}")
        return None
    return session

def load_cookies(session):
    if os.path.exists('cookies.txt'):
        with open('cookies.txt', 'r') as file:
            cookies = eval(file.read())
            session.cookies.update(cookies)
        logging.info("Cookies loaded from file.")

def scrape_torrents(session):
    torrents_url = "https://hdfans.org/torrents.php"
    leeching_pattern = re.compile(r"leeching")
    ignored_titles = [
        "Downton.Abbey.A.New.Era.2022.2160p.WEB-DL.DDP5.1.Atmos.HDR.DV.x265-HDFans",
        "Great British Railway Journeys S01-S13 720p HDTV x264-Mixed",
        "King Arthur 2004 Extended Director's Cut Bluray 1080p x265.10bit DDP 5.1-WGXC@HDFans",
        "Prince of Persia the Sands of Time 2010 BluRay 1080p x265 2Audio-WGXC@HDFans"
    ]

    try:
        response = session.get(torrents_url)
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            torrents = soup.find_all('td', class_='embedded')
            ignored_titles_count = 0

            for torrent in torrents:
                title_element = torrent.find('a')
                if title_element and title_element.get('title') in ignored_titles:
                    ignored_titles_count += 1
                    if ignored_titles_count <= 4:
                        logging.info(f"Ignoring torrent: {title_element['title']}")
                        continue
                    else:
                        break  # Stop after ignoring the specified number of titles

                # Check if the torrent is leeching
                if any(leeching_pattern.search(div.get('title', '')) for div in torrent.find_all('div')):
                    logging.info("Leeching torrent found. Stopping processing.")
                    break

                # Process eligible torrents
                if torrent.find('img', class_='pro_free2up'):
                    torrent_id = title_element['href'].split('=')[1].split('&')[0] if title_element else None
                    if torrent_id:
                        logging.info(f"Processing torrent: {title_element['title']}")
                        download_torrent(session, torrent_id)

        else:
            logging.error("Failed to load torrents page")
    except requests.RequestException as e:
        logging.error(f"Error scraping torrents: {e}")


def download_torrent(session, torrent_id):
    download_url = f"https://hdfans.org/download.php?id={torrent_id}"
    try:
        response = session.get(download_url)
        if response.ok:
            with open(f'{torrent_id}.torrent', 'wb') as file:
                file.write(response.content)
            logging.info(f"Downloaded {torrent_id}.torrent")
        else:
            logging.error(f"Failed to download torrent {torrent_id}")
    except requests.RequestException as e:
        logging.error(f"Error downloading torrent {torrent_id}: {e}")
def clear_log_file():
    log_file_path = 'hdfans.log'
    try:
        # Open the file in write mode to truncate it
        with open(log_file_path, 'w'):
            logging.info("Log file cleared.")
    except OSError as e:
        logging.error(f"Error clearing log file: {e}")
def main():
    session = requests.Session()

    if not os.path.exists('cookies.txt'):
        hash_value = imageHash(session)
        if hash_value:
            solution = solve(hash_value)
            if solution:
                session = login_and_save_cookies(solution, hash_value)
                if not session:
                    logging.error("Failed to log in")
                    return
            else:
                logging.error("Failed to solve CAPTCHA")
                return
        else:
            logging.error("Failed to retrieve image hash")
            return

    load_cookies(session)

    while True:
        logging.info("Scraping torrents...")
        scrape_torrents(session)
        logging.info("Waiting for next scrape cycle...")
        time.sleep(600)
        clear_log_file()

if __name__ == "__main__":
    main()
