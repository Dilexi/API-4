import os
from pathlib import Path

import requests
from urllib.parse import urlparse, unquote

from dotenv import load_dotenv
from download_image import download_image


def extract_extension_from_link(link):
    decoded_link = unquote(link)
    parsed_link = urlparse(decoded_link)
    path, fullname = os.path.split(parsed_link.path)
    file_extension_path = os.path.splitext(fullname)
    file_name, extension = file_extension_path
    return extension, file_name


def get_nasa_images(nasa_api_key, folder_name, links_count):
    nasa_link_apod = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": nasa_api_key,
        "count": links_count
    }
    response = requests.get(nasa_link_apod, params=params)
    response.raise_for_status()
    nasa_images = response.json()
    for image_nasa in nasa_images:
        if image_nasa.get("media_type") == "image":
            if image_nasa.get("hdurl"):
                nasa_link_image = image_nasa["hdurl"]
            else:
                nasa_link_image = image_nasa["url"]
            print(nasa_link_image)
            extension, file_name = extract_extension_from_link(nasa_link_image)
            path = os.path.join(folder_name, f'{file_name}{extension}')
            download_image(nasa_link_image, path)


def main():
    links_count = int(input("Введите необходимо количество фотографий: "))
    load_dotenv()
    nasa_api_key = os.environ['NASA_TOKEN']
    folder_name = os.environ.get("FOLDER_NASA_APOD", "nasa_apod_photos")
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    get_nasa_images(folder_name, nasa_api_key, links_count)


if __name__=="__main__":
    main()
