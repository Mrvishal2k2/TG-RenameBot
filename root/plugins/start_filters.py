'''
RenameBot
Thanks to Spechide Unkle as always for the concept  ♥️
This file is a part of mrvishal2k2 rename repo 
Dont kang !!!
© Mrvishal2k2
'''
import os, logging
log = logging.getLogger(__name__)

from pyrogram import Client,filters
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from root.config import Config
from root.messages import Translation

@Client.on_message(filters.command("start"))
async def start_msg(c,m):
    try:
       await m.reply_text(
            text=Translation.START_TEXT,
            quote=True, 
            reply_markup=InlineKeyboardMarkup([[
               InlineKeyboardButton(
               "Owner ", 
               url=f"https://t.me/{Config.OWNER_USERNAME}")
                "Update_Channel"
                url=f"https://t.me/DL_Bots_Update")
             ]]) , 
            disable_web_page_preview=True
      ) 
    except Exception as e:
        log.error(str(e))

@Client.on_message(filters.command("help"))
async def help_user(c,m):
    try:
       await m.reply_text(text=Translation.HELP_USER,quote=True)
    except Exception as e:
        log.info(str(e))


@Client.on_message(filters.command("log") & filters.private & filters.user(Config.OWNER_ID))
async def log_msg(c,m):
  z =await m.reply_text("Processing..", True)
  if os.path.exists("Log.txt"):
     await m.reply_document("Log.txt", True)
     await z.delete()
  else:
    await z.edit_text("Log file not found")
