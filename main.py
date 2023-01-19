import logging
from os import getenv

from dotenv import load_dotenv

from core import VRBot

load_dotenv()

if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)

    bot = VRBot()
    bot.run(getenv("TOKEN"))
