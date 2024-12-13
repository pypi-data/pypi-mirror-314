import argparse
import os
import requests
from datetime import datetime

def upload_image(filepath, index, total):
    if not os.path.isfile(filepath):
        print(f"Error: File not found - {filepath}")
        return None

    print(f"Uploading {index}/{total}")
    url = "https://imgbb.com/json"
    timestamp = str(int(datetime.now().timestamp()))

    with open(filepath, 'rb') as file:
        files = {
            'source': file,
            'type': (None, "file"),
            'action': (None, "upload"),
            'timestamp': (None, timestamp)
        }
        response = requests.post(url, files=files)

    if response.status_code == 200:
        data = response.json()
        return data['image']['url']
    else:
        print(f"Failed to upload image: {filepath}. Status code: {response.status_code}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Upload images to imgbb")
    parser.add_argument("filepaths", nargs='+', type=str, help="Paths to the image files")
    args = parser.parse_args()

    total_files = len(args.filepaths)
    print(f"Total of {total_files} file paths and URLs")
    print("Uploading...")

    uploaded_urls = []

    for index, filepath in enumerate(args.filepaths, start=1):
        url = upload_image(filepath, index, total_files)
        if url:
            uploaded_urls.append(url)

    print("Output URLs:")
    for url in uploaded_urls:
        print(url)

if __name__ == "__main__":
    main()