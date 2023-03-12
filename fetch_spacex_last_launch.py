import os
from pathlib import Path

import requests

from dotenv import load_dotenv
from download_image import download_image


def fetch_spacex_last_launch(folder_name):
    image_link = "https://api.spacexdata.com/v5/launches/"
    response = requests.get(image_link)
    response.raise_for_status()
    
    for link_photo_spasex in response.json():
        if link_photo_spasex["links"]['flickr']["original"]:
            urls_photo=link_photo_spasex["links"]['flickr']["original"]

    for number, link in enumerate(urls_photo):
        file_name = f"spacex_{number}.jpg"
        path = os.path.join(folder_name, file_name)
        download_image(link, path)


def main():
    load_dotenv()
    folder_name = os.environ['FOLDER_SPACEX']
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    fetch_spacex_last_launch(folder_name)


if __name__=="__main__":
    main()
