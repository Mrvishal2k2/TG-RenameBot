'''
RenameBot
© Mrvishal2k2
'''
import os
import logging

if os.path.exists(".env"):
    for line in open(".env"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())
from logging.handlers import RotatingFileHandler
from pyrogram import Client
from Bot.config import Config

# Rotate old log on startup
if os.path.exists("Log.txt"):
    with open("Log.txt", "r+") as f:
        f.truncate(0)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("Log.txt", maxBytes=1_000_000, backupCount=5),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
log = logging.getLogger(__name__)


class RenameBot(Client):
    def __init__(self):
        super().__init__(
            name="RenameBot",
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.TG_BOT_TOKEN,
            plugins={"root": "Bot/plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        await super().start()
        os.makedirs(Config.DOWNLOAD_LOCATION, exist_ok=True)
        os.makedirs(os.path.join(Config.DOWNLOAD_LOCATION, "thumb"), exist_ok=True)
        me = await self.get_me()
        log.info(f"Bot started as @{me.username}")

    async def stop(self, *args):
        await super().stop()
        log.info("Bot stopped.")


RenameBot().run()
