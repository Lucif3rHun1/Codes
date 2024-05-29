import requests
import os
from datetime import datetime

# Create a session object
session = requests.Session()

# Disable cache
session.headers.update({"Cache-Control": "no-cache"})

# Define headers
seedr_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Accept": "application/json, text/plain, */*",
    "Cookie": "RSESS_remember=28cc98be6ee635bdf600de1bd87eb14f8c261640; PHPSESSID=6978b2a5e2b629c6b59737b2d2b21d20; _pk_id.2.5294=319b9fdb23f75b5f.1694882660.; _pk_ses.2.5294=1; amp_6e403e=Zebkeb_OxuUevOmWJ5S9Y8...1hakmtbje.1hakmted4.0.0.0"
}

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Output folder path
output_folder = script_dir

# Define the folder ID file path
folder_id_file = os.path.join(script_dir, "seedr_folder_id.txt")
def create_output_folder():
    """Create the output folder if it doesn't exist."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
def create_or_get_existing_seedr_folder():
    """Create a new Seedr folder or retrieve an existing one with the same name."""
    folder_name = "Lucif3rHun1"
    try:
        folder_items_url = "https://www.seedr.cc/fs/folder/0/items"
        folder_items_response = session.get(folder_items_url, headers=seedr_headers)
        folder_items_response.raise_for_status()

        if folder_items_response.status_code == 200:
            folder_items_data = folder_items_response.json()
            folders = folder_items_data.get("folders", [])

            for folder in folders:
                if folder.get("path") == folder_name:
                    folder_id = folder.get("id")
                    print("Folder name already taken. Using existing folder. Folder ID:", folder_id)
                    save_seedr_folder_id(folder_id)
                    return folder_id

            # If folder with the same name doesn't exist, create a new one
            seedr_folder_url = "https://www.seedr.cc/fs/folder"
            seedr_folder_data = {
                "name": folder_name
            }

            response = session.post(seedr_folder_url, data=seedr_folder_data, headers=seedr_headers, allow_redirects=True)
            response.raise_for_status()

            if response.status_code == 200:
                seedr_response_data = response.json()
                folder_id = seedr_response_data.get("id")
                if folder_id:
                    print("Seedr Folder created successfully. Folder ID:", folder_id)
                    save_seedr_folder_id(folder_id)
                    return folder_id
                else:
                    print("Error creating Seedr Folder:", seedr_response_data.get("error"))

            else:
                print("Error in Seedr Folder response:", response.text)

        else:
            print("Error retrieving folder items:", folder_items_response.text)

    except requests.exceptions.RequestException as e:
        print("Error during Seedr Folder creation:", e)

    return None

def get_seedr_folder_id():
    """Retrieve the Seedr folder ID from the seedr_folder_id.txt file."""
    if os.path.isfile(folder_id_file):
        with open(folder_id_file, "r") as file:
            return file.read().strip()
    return None

def save_seedr_folder_id(folder_id):
    """Save the Seedr folder ID to the seedr_folder_id.txt file."""
    with open(folder_id_file, "w") as file:
        file.write(str(folder_id))

def get_folder_items(folder_id):
    """Retrieve the folder items of the specified Seedr folder ID."""
    try:
        folder_items_url = f"https://www.seedr.cc/fs/folder/{folder_id}/items"
        response = session.get(folder_items_url, headers=seedr_headers)
        response.raise_for_status()

        if response.status_code == 200:
            folder_items_data = response.json()
            return folder_items_data

        else:
            print("Error in folder items response:", response.text)

    except requests.exceptions.RequestException as e:
        print("Error getting folder items:", e)

    return None

def download_file(file_id):
    """Download the file with the specified file ID and retrieve the download URL."""
    try:
        download_url = f"https://www.seedr.cc/download/file/{file_id}/url"
        response = session.get(download_url, headers=seedr_headers)
        response.raise_for_status()

        if response.status_code == 200:
            download_data = response.json()
            download_url = download_data.get("url")
            return download_url

        else:
            print("Error in file download response:", response.text)

    except requests.exceptions.RequestException as e:
        print("Error during file download:", e)

    return None

def process_files(files, output_file):
    """
    Process the list of files, download the ones identified as videos,
    and save their download URLs to the output file. Track statistics.
    """
    total_files = len(files)
    video_files = 0

    with open(output_file, "a") as file:
        for file_item in files:
            file_id = file_item.get("id")
            file_name = file_item.get("name")
            is_video = file_item.get("is_video")
            if is_video:
                download_url = download_file(file_id)
                if download_url:
                    file.write(f"{file_name}: {download_url}\n")
                    video_files += 1
                    print(f"Download URL for {file_name} saved.")
            else:
                print(f"Skipping file {file_name} as it is not a video.")

    return total_files, video_files, total_files - video_files

def process_folder_items(folder_id, output_file):
    """
    Recursively process the folder items of the specified Seedr folder ID,
    including nested folders, and save the download URLs of video files.
    Track statistics for the entire folder structure.
    """
    folder_items_data = get_folder_items(folder_id)
    if folder_items_data:
        total_files = 0
        video_files = 0
        skipped_files = 0

        total_files += len(folder_items_data.get("files", []))
        video_files += sum(1 for file_item in folder_items_data.get("files", []) if file_item.get("is_video"))
        skipped_files += sum(1 for file_item in folder_items_data.get("files", []) if not file_item.get("is_video"))

        with open(output_file, "a") as file:
            for file_item in folder_items_data.get("files"):
                file_id = file_item.get("id")
                file_name = file_item.get("name")
                is_video = file_item.get("is_video")
                if is_video:
                    download_url = download_file(file_id)
                    if download_url:
                        file.write(f"{download_url}\n")
                        video_files += 1
                        print(f"Download URL for {file_name} saved.")
                else:
                    print(f"Skipping file {file_name} as it is not a video.")

        for folder_item in folder_items_data.get("folders"):
            nested_folder_id = folder_item.get("id")
            sub_total, sub_video, sub_skipped = process_folder_items(nested_folder_id, output_file)
            total_files += sub_total
            video_files += sub_video
            skipped_files += sub_skipped

        return total_files, video_files, skipped_files

    return 0, 0, 0

def main():
    """Main execution logic."""
    create_output_folder()

    folder_id = get_seedr_folder_id()
    if not folder_id:
        folder_id = create_or_get_existing_seedr_folder()
        if not folder_id:
            print("Failed to create or get Seedr folder.")
            return

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = os.path.join(output_folder, f"seedr_links_{timestamp}.txt")

    # Create the output file before saving download URLs
    open(output_file, "w").close()

    total_files, video_files, skipped_files = process_folder_items(folder_id, output_file)

    print("Overall Statistics:")
    print(f"Total Files: {total_files}, Video Files: {video_files-skipped_files}, Skipped Files: {skipped_files}")

    # Display currently queued torrents count
    folder_items_data = get_folder_items(folder_id)
    if folder_items_data:
        torrents_data = folder_items_data.get("torrents", [])
        currently_queued_torrents = len(torrents_data)
        print(f"Currently Queued Torrents: {currently_queued_torrents}")

    print(f"All download URLs saved in {output_file}.")

if __name__ == "__main__":
    main()