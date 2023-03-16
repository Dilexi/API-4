import os
from pathlib import Path

import requests
from urllib.parse import urlparse, unquote

from dotenv import load_dotenv
from download_image import download_image


def extract_extension_from_link(link):
    link_unquote = unquote(link)
    link_parse =  urlparse(link_unquote)
    path, fullname = os.path.split(link_parse.path)
    file_extension_path = os.path.splitext(fullname)
    file_name, extension = file_extension_path
    return extension, file_name


def get_nasa_images(folder_nasa, nasa_api_key, folder_name):
    nasa_link_apod = "https://api.nasa.gov/planetary/apod"
    links_count = 3
    params = {
        "api_key": nasa_api_key,
        "count": links_count
    }
    response = requests.get(nasa_link_apod, params=params)
    response.raise_for_status()
    nasa_images = response.json()
    for image_nasa in nasa_images:
        if image_nasa["url"]:
            nasa_link_image = image_nasa["url"]
            print(nasa_link_image)
            extension, file_name = extract_extension_from_link(nasa_link_image)
            path = os.path.join(folder_name, f'{file_name}{extension}')
            download_image(nasa_link_image, path)


def main():
    load_dotenv()
    nasa_api_key = os.environ['NASA_API']
    folder_name = os.environ['FOLDER_NASA_APOD']
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    get_nasa_images(folder_name, api_key,folder_name)


if __name__=="__main__":
    main()
