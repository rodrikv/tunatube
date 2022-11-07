import os
import dotenv

from time import sleep
from telegram.error import TimedOut
from tunatube.client.telegram import TunaTubeBot
from tunatube.client.telethon import TunaTubeClient


dotenv.load_dotenv()

if __name__ == "__main__":
    ttclient = TunaTubeClient(os.getenv("API_ID"), os.getenv("API_HASH"), os.getenv("TOKEN"))
    ttbot = TunaTubeBot(os.getenv("TOKEN"))
    ttbot.client = ttclient

    while True:
        try:
            ttbot.run()
            break

        except TimedOut:
            print("Restarting in 3 seconds...")
            sleep(3)