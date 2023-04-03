import os
import argparse
from datetime import datetime
from pathlib import Path

import requests

from dotenv import load_dotenv
from download_image import download_image


def get_epic_nasa_images(folder_name, nasa_api_key, links_count):
    link_epic = "https://api.nasa.gov/EPIC/api/natural/image"
    params = {
        "api_key": nasa_api_key,
        "count": links_count
    }

    response = requests.get(
        link_epic,
        params = params
    )
    
    response.raise_for_status()
    epic_images = response.json()
    
    for epic_image in epic_images:
        file_name = epic_image["image"]
        epic_image_date = epic_image["date"]
        epic_image_date = datetime.fromisoformat(epic_image_date).strftime("%Y/%m/%d")
        link_path = f"https://api.nasa.gov/EPIC/archive/natural/{epic_image_date}/png/{file_name}.png"
        path = os.path.join(folder_name, f'{file_name}.png')
        download_image(link_path, path, params)


def main():
    parser = argparse.ArgumentParser(description='Загружает изображения NASA APOD')
    parser.add_argument('count', type=int, help='Введите необходимо колличество фотографий:')
    args = parser.parse_args()
    load_dotenv()
    nasa_api_key = os.environ['NASA_TOKEN']
    folder_name = os.environ.get("FOLDER_EPIC", "epic_photos")
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    get_epic_nasa_images(folder_name, nasa_api_key, args.count)


if __name__=="__main__":
    main()
