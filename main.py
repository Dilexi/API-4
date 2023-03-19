import os
import telegram
import random
from os import listdir
from time import sleep
from telegram.error import NetworkError


def main():
    tg_token = os.environ['TG_TOKEN']
    tg_chat_id = os.environ['TG_CHAT_ID']
    folder_spacex = os.environ.get("FOLDER_SPACEX", "spacex_photos")
    folder_nasa_apod = os.environ.get("FOLDER_NASA_APOD", "nasa_apod_photos")
    folder_epic = os.environ.get("FOLDER_EPIC", "epic_photos")
    publish_delay = int(os.environ.get('PUBLISH_DELAY', 14400))
    bot = telegram.Bot(token=tg_token)
    while True:
        try:
            folders = [
                folder_spacex,
                folder_nasa_apod,
                folder_epic
            ]
            folder = random.choice(folders)
            files = listdir(folder)
            random.shuffle(files)
            for file in files:
                filepath = os.path.join(folder, file)
                with open(filepath, 'rb') as f:
                    bot.send_document(chat_id=tg_chat_id, document=f)
                sleep(publish_delay)
        except NetworkError:
            print("Ошибка сети. Повторная попытка через 20 секунд...")
            sleep(20)


if __name__ == "__main__":
    main()
