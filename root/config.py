'''
© Mrvishal2k2
RenameBot
This file is a part of mrvishal2k2 rename repo 
Dont kang !!!
© Mrvishal2k2
'''
import os 

class Config(object):
  APP_ID = int(os.environ.get("APP_ID", ""))
  API_HASH = os.environ.get("API_HASH", "")
  TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
  AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "").split())
  DOWNLOAD_LOCATION = "./bot/DOWNLOADS"
  DB_URI = os.environ.get("DATABASE_URL", "")
  # owner is for log cmd only owner can use (this can be multiple users)
  OWNER_ID = [int(i) for i in os.environ.get("OWNER_ID", "").split(" ")]
  OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "BotDunia")
  CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION",False)
