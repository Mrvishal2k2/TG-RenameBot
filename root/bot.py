# RenameBot
# This file is a part of mrvishal2k2 rename repo 
# Dont kang !!!
# © Mrvishal2k2

import logging
import os
from config import Config
from logging.handlers import RotatingFileHandler

if os.path.exists("Log.txt"):
    with open("Log.txt", "r+") as f_d:
        f_d.truncate(0)


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt="%d-%b-%y %H:%M:%S",
                    handlers=[
        RotatingFileHandler(
            "Log.txt",
            maxBytes=1000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)

log = logging.getLogger(__name__)

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

if __name__ == "__main__" :
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    plugins = dict(
        root="root/plugins"
    )
    BOT = pyrogram.Client(
        "RenameBot",
        bot_token=Config.TG_BOT_TOKEN,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        plugins=plugins
    )
    log.info("<<[Bot Started]>>")
    BOT.run()
