import requests
import tkinter as tk
import pyperclip
from tkinter import scrolledtext
import threading
import re
import logging
import urllib3
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class SeedrManager:
    def __init__(self, headers, folder_name):
        self.session = requests.Session()
        self.session.headers.update({"Cache-Control": "no-cache"})
        self.headers = headers
        self.session.verify = False
        self.folder_name = folder_name
        self.folder_id = 281774667

    def create_seedr_folder(self):
        try:
            # Check if the folder already exists
            folder_id = self.get_existing_folder_id()
            if folder_id:
                self.folder_id = folder_id
                return True

            # If folder does not exist, create a new one
            seedr_folder_url = "https://www.seedr.cc/fs/folder"
            seedr_folder_data = {"name": self.folder_name}
            response = self.session.post(seedr_folder_url, data=seedr_folder_data, headers=self.headers, allow_redirects=True)
            response.raise_for_status()

            if response.status_code == 200:
                seedr_response_data = response.json()
                if "error" in seedr_response_data:
                    return False

                self.folder_id = seedr_response_data["id"]
                return True

            else:
                return False

        except requests.exceptions.RequestException as e:
            logging.error("Error during Seedr folder creation:", exc_info=True)
            return False

    def get_existing_folder_id(self):
        items_url = "https://www.seedr.cc/fs/folder/0/items"
        try:
            items_response = self.session.get(items_url, headers=self.headers)
            items_response.raise_for_status()
            items_data = items_response.json()
            folders = items_data.get("folders", [])
            for folder in folders:
                if folder["path"] == self.folder_name:
                    return folder["id"]
            return None
        except requests.exceptions.RequestException as e:
            logging.error("Error while fetching existing folders:", exc_info=True)
            return None
            
    def create_seedr_task(self, magnet_link):
        seedr_task_url = "https://www.seedr.cc/task"
        seedr_task_data = {
            "folder_id": self.folder_id,
            "type": "torrent",
            "torrent_magnet": magnet_link
        }
        try:
            response = self.session.post(seedr_task_url, data=seedr_task_data, headers=self.headers, allow_redirects=True)
            response.raise_for_status()

            if response.status_code == 200:
                seedr_task_response_data = response.json()
                if seedr_task_response_data.get("success") == True:
                    return "Seedr Task created successfully."
                elif "reason_phrase" in seedr_task_response_data:
                    return seedr_task_response_data["reason_phrase"]
            elif response.status_code == 409:  # Conflict
                return "Conflict: Seedr Task already exists."

            return "Error in Seedr Task response."

        except requests.exceptions.RequestException as e:
            logging.error("Error during Seedr task creation:", exc_info=True)
            error_msg = f"Error during Seedr Task creation: {str(e)}"
            if response and response.text:
                error_msg += f"\nResponse content: {response.text}"
            return error_msg

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Seedr Manager")
        self.geometry("1080x900")

        self.counters = {
            "Total": tk.StringVar(value="Total: 0"),
            "Success": tk.StringVar(value="Success: 0"),
            "Duplicate": tk.StringVar(value="Duplicate: 0"),
            "Conflict": tk.StringVar(value="Conflict: 0"),
            "Error": tk.StringVar(value="Error: 0")
        }

        self.seedr_manager = SeedrManager({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Accept": "application/json, text/plain, */*",
            "Cookie": "PHPSESSID=a2d6c64eac1be2cc7b732101b1b72084; RSESS_session=136bc65bd72ace3037d1a2ce7db6f37ea5567ddc; RSESS_remember=892bf0be3fa6ba91cb4d4a379d86cef3ed9bc428; amp_6e403e=Zebkeb_OxuUevOmWJ5S9Y8...1h7k8vm6g.1h7k94bfp.0.0.0",
        }, "Lucif3rHun1")

        self.create_widgets()
        self.last_paste = set()  # To store the links from the last paste

    def create_widgets(self):
        label = tk.Label(self, text="Magnet Link:", font=('Arial', 14))
        label.pack(pady=10)

        self.magnet_entry = tk.Entry(self, font=('Arial', 14), width=50)
        self.magnet_entry.pack(pady=5)
        self.magnet_entry.bind("<Button-1>", self.handle_paste)

        self.log_text = tk.Text(self, height=20, width=80, wrap=tk.WORD)
        self.log_text.pack()

        self.counters_label = tk.Label(self, text="", font=('Arial', 14))
        self.counters_label.pack(pady=5)

        quit_button = tk.Button(self, text="QUIT", fg="red", command=self.destroy, font=('Arial', 14), bg='lightgrey')
        quit_button.pack(pady=5)

    def handle_paste(self, event):
        clipboard_content = pyperclip.paste()
        magnet_links = clipboard_content.strip().split("\n")
        unique_magnet_links = set(magnet_links)

        if len(unique_magnet_links) == 1:
            self.process_single_paste(unique_magnet_links.pop())
        else:
            threading.Thread(target=self.process_batch_paste, args=(unique_magnet_links,)).start()

    def process_single_paste(self, magnet_link):
        self.log("=== Processing Single Paste ===")
        self.process_link(magnet_link)
        self.log("=== Single Paste Completed ===")

    def process_batch_paste(self, magnet_links):
        self.log("=== Processing Batch Paste ===")
        total_links = len(magnet_links)
        self.reset_counters()  # Reset the counters for the current batch

        unique_magnet_links = self.remove_duplicates(magnet_links)  # Remove duplicates from the current paste
        
        self.counters["Total"].set(f"Total: {total_links}")  # Update the total count
        
        for index, magnet_link in enumerate(unique_magnet_links, start=1):
            if self.is_valid_magnet_link(magnet_link):
                self.process_link(magnet_link)
                self.log_counters(index, total_links)
                self.update()

        self.log_final_counters()  # Log the dynamic counter's final count
        self.log("=== Batch Paste Completed ===")
        self.counters_label.config(text="")  # Clear counters label

    def remove_duplicates(self, magnet_links):
        new_magnet_links = []
        for link in magnet_links:
            if link not in self.last_paste:
                new_magnet_links.append(link)
        self.last_paste = set(magnet_links)
        return new_magnet_links

    def reset_counters(self):
        for counter in self.counters.values():
            counter.set(f"{counter.get().split(':')[0]}: 0")

    def process_link(self, magnet_link):
        try:
            attempts = 3
            result = ""
            while attempts > 0:
                result = self.seedr_manager.create_seedr_task(magnet_link)
                if "successfully" in result:
                    self.counters["Success"].set(f"Success: {int(self.counters['Success'].get().split(':')[1]) + 1}")
                    break
                elif "Conflict" in result:
                    self.counters["Conflict"].set(f"Conflict: {int(self.counters['Conflict'].get().split(':')[1]) + 1}")
                    break
                elif attempts > 1:
                    logging.warning("Retrying after 2 seconds...")
                    time.sleep(2)
                attempts -= 1

            if attempts == 0:
                self.counters["Error"].set(f"Error: {int(self.counters['Error'].get().split(':')[1]) + 1}")

        except requests.exceptions.RequestException as e:
            self.counters["Error"].set(f"Error: {int(self.counters['Error'].get().split(':')[1]) + 1}")
            logging.error(f"Error during Seedr task creation: {str(e)}")

    def log_counters(self, index, total_links):
        counters_text = f"Total: {index} / {total_links} | {self.counters['Success'].get()} | {self.counters['Duplicate'].get()} | {self.counters['Conflict'].get()} | {self.counters['Error'].get()}"
        self.counters_label.config(text=counters_text)
        self.update()

    def log_final_counters(self):
        final_counters_text = f"Total: {int(self.counters['Total'].get().split(':')[1])} | {self.counters['Success'].get()} | {self.counters['Duplicate'].get()} | {self.counters['Conflict'].get()} | {self.counters['Error'].get()}"
        self.log(final_counters_text)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)  # Scroll to the end of the log

    def is_valid_magnet_link(self, link):
        pattern = r'^magnet:\?xt=urn:btih:[a-fA-F0-9]{40}.*$'
        return re.match(pattern, link) is not None


if __name__ == "__main__":
    app = Application()
    app.mainloop()