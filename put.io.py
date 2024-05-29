import requests
import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Setup Logging
logging.basicConfig(filename='putio_uploader.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

PUTIO_API_TOKEN = 'CNXXBQPWTGRPW2PHCDMT'
UPLOAD_URL = 'https://upload.put.io/files/'
FILES_URL = 'https://api.put.io/v2/files/list'
DELETE_URL = 'https://api.put.io/v2/files/delete'
TORRENT_FOLDER = '/Users/lucif3rhun1/Downloads/Torrents'

class TorrentHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.torrent'):
            try:
                upload_torrent(event.src_path)
            except Exception as e:
                logging.error(f"Error uploading file {event.src_path}: {e}")

def upload_torrent(file_path):
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(UPLOAD_URL, files=files, headers={'Authorization': f'token {PUTIO_API_TOKEN}'})
        if response.status_code == 200:
            logging.info(f"Uploaded {file_path}")
            os.remove(file_path)
        else:
            logging.error(f"Failed to upload {file_path}: {response.text}")
    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
    except OSError as e:
        logging.error(f"File error: {e}")

def check_storage_and_cleanup():
    try:
        response = requests.get(FILES_URL, headers={'Authorization': f'token {PUTIO_API_TOKEN}'})
        if response.status_code == 200:
            data = response.json()
            # Implement storage check and file deletion logic here
        else:
            logging.error(f"Error fetching file list: {response.text}")
    except requests.RequestException as e:
        logging.error(f"Request error: {e}")

def main():
    logging.info("Starting put.io uploader service")
    event_handler = TorrentHandler()
    observer = Observer()
    observer.schedule(event_handler, TORRENT_FOLDER, recursive=False)
    observer.start()
    try:
        while True:
            check_storage_and_cleanup()
            time.sleep(600)  # Check every 10 minutes
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Stopping put.io uploader service")
    observer.join()

if __name__ == "__main__":
    main()
