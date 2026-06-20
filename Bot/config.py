'''
RenameBot
© Mrvishal2k2
'''
import os


class Config:
    APP_ID = int(os.environ["APP_ID"])
    API_HASH = os.environ["API_HASH"]
    TG_BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
    # Space-separated user IDs that can use the bot; empty = everyone
    AUTH_USERS = [int(x) for x in os.environ.get("AUTH_USERS", "").split() if x]
    DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./Bot/DOWNLOADS")
    DB_URI = os.environ.get("DATABASE_URL")
    # Space-separated owner IDs (can use /log)
    OWNER_ID = [int(i) for i in os.environ.get("OWNER_ID", "0").split() if i]
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "")
    CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "")
