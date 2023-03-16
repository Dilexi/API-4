import os
import telegram
import random
from os import listdir
from time import sleep


def main():
    TG_TOKEN = os.environ['TG_TOKEN']
    TG_CHAT_ID = os.environ['TG_CHAT_ID']
    FOLDER_SPACEX = os.environ["FOLDER_SPACEX"]
    FOLDER_NASA = os.environ["FOLDER_NASA_APOD"]
    FOLDER_EPIC = os.environ["FOLDER_EPIC"]
    PUBLISH_DELAY = int(os.environ.get('PUBLISH_DELAY', 14400))
    bot = telegram.Bot(token=TG_TOKEN)
    while True:
        folders = [
            FOLDER_SPACEX,
            FOLDER_NASA,
            FOLDER_EPIC
        ]
        folders = random.choice(folders)
        files = listdir(folders)
        random.shuffle(files)
        for file in files:
            bot.send_document(chat_id=TG_CHAT_ID,
                    document=open(f'{folders}/{file}', 'rb'))
            sleep(PUBLISH_DELAY)


if __name__ == "__main__":
    main()
