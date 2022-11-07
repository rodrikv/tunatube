import os
import dotenv

from time import sleep
from telegram.error import TimedOut
from tunatube.client.telegram import TunaTubeBot


dotenv.load_dotenv()

if __name__ == "__main__":
    ttbot = TunaTubeBot(os.getenv("TOKEN"))
    while True:
        try:
            ttbot.run()
            break

        except TimedOut:
            print("Restarting in 3 seconds...")
            sleep(3)