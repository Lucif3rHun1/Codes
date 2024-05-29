import os
import threading
from pySmartDL import SmartDL
from tqdm import tqdm

class DownloadThread(threading.Thread):
    def __init__(self, url, save_path, custom_name):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.custom_name = custom_name

    def run(self):
        try:
            file_name = self.custom_name or os.path.basename(self.url)
            file_path = os.path.join(self.save_path, file_name)

            obj = SmartDL(self.url, file_path)
            obj.start()

            while not obj.isFinished():
                obj.wait()
                progress = obj.get_progress()
                tqdm.write(f"Downloading {file_name}: {progress}%")

            if obj.isSuccessful():
                print(f"Downloaded: {self.url} -> {file_path}")
            else:
                print(f"Failed to download: {self.url}")

        except Exception as e:
            print(f"Error downloading {self.url}: {str(e)}")

def main():
    # Read links and custom names from the text file
    with open('download_list.txt', 'r') as file:
        lines = file.readlines()

    urls = []
    for line in lines:
        parts = line.split('-', 1)  # Split only at the first hyphen
        link = parts[0].strip()
        name = parts[1].strip() if len(parts) > 1 else None
        urls.append((link, name))

    save_path = 'downloads'  # Folder where downloads will be saved

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    threads = []
    for url, custom_name in urls:
        thread = DownloadThread(url, save_path, custom_name)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All downloads completed.")

if __name__ == "__main__":
    main()
