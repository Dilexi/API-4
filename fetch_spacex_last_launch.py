import os
import argparse
from pathlib import Path

import requests

from dotenv import load_dotenv
from download_image import download_image


def get_spacex_photo_links(launch_id=None):
    if launch_id:
        image_link = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    else:
        image_link = "https://api.spacexdata.com/v5/launches/"
    response = requests.get(image_link)
    response.raise_for_status()
    
    if launch_id:
        photo_urls=response.json()['links']['flickr']['original']
    else:
        for link_photo_spaсex in response.json():
            if link_photo_spaсex["links"]['flickr'] and link_photo_spaсex["links"]['flickr']["original"]:
                photo_urls=link_photo_spaсex["links"]['flickr']["original"]
    return photo_urls


def save_photos_to_folder(photo_urls, folder_name):
    for number, link in enumerate(photo_urls):
        file_name = f"spacex_{number}.jpg"
        path = os.path.join(folder_name, file_name)
        download_image(link, path)


def fetch_spacex_last_launch(folder_name, launch_id=None):
    links = get_spacex_photo_links(launch_id)
    save_photos_to_folder(links, folder_name)
    
 
def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
        description='Эта программа позволит вам загрузитть фотографии с запуска SpaceX.'
    )
    parser.add_argument(
        '--id',
        dest='launch_id',
        default=None,
        help='Укажите ID запуска SpaceX, с которого можно загрузить фотографии.'
    )
    args = parser.parse_args()
    folder_name = os.environ.get("FOLDER_SPACEX", "spacex_photos")
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    fetch_spacex_last_launch(folder_name, args.launch_id)


if __name__=="__main__":
    main()
