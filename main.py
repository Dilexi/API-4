import os
import telegram
import random
from os import listdir
from time import sleep
from telegram.error import NetworkError


def main():
    TG_TOKEN = os.environ['TG_TOKEN']
    TG_CHAT_ID = os.environ['TG_CHAT_ID']
    FOLDER_SPACEX = os.environ.get("FOLDER_SPACEX", "spacex_photos")
    FOLDER_NASA_APOD = os.environ.get("FOLDER_NASA_APOD", "nasa_apod_photos")
    FOLDER_EPIC = os.environ.get("FOLDER_EPIC", "epic_photos")
    PUBLISH_DELAY = int(os.environ.get('PUBLISH_DELAY', 14400))
    bot = telegram.Bot(token=TG_TOKEN)
    while True:
        try:
            folders = [
                FOLDER_SPACEX,
                FOLDER_NASA_APOD,
                FOLDER_EPIC
            ]
            folder = random.choice(folders)
            files = listdir(folder)
            random.shuffle(files)
            for file in files:
                filepath = os.path.join(folder, file)
                with open(filepath, 'rb') as f:
                    bot.send_document(chat_id=TG_CHAT_ID, document=f)
                sleep(PUBLISH_DELAY)
        except NetworkError:
            print("Ошибка сети. Повторная попытка через 20 секунд...")
            sleep(20)


if __name__ == "__main__":
    main()
