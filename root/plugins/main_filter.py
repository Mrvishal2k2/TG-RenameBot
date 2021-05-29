'''
RenameBot
This file is a part of mrvishal2k2 rename repo 
Dont kang !!!
© Mrvishal2k2
'''
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

@Client.on_message(filters.document | filters.video | filters.audio | filters.voice | filters.video_note | filters.animation) 
async def rename_filter(c,m):
  media = m.document or m.video or m.audio or m.voice or m.video_note or m.animation
  ## couldn't add photo bcoz i want all photos to use as thumb..
  
  text = ""
  button = []
  try:
    filename = media.file_name
    text += f"FileName:\n{filename}\n"
  except:
    # some files dont gib name ..
    filename = None 
    
  text += "Select the desired Option"
  button.append([InlineKeyboardButton("Rename as File", callback_data="rename_file")])
  # Thanks to albert for mime_type suggestion 
  if media.mime_type.startswith("video/"):
    ## how the f the other formats can be uploaded as video 
    button.append([InlineKeyboardButton("Rename as Video",callback_data="rename_video")])
    button.append([InlineKeyboardButton("Convert as File",callback_data="convert_file")])
    button.append([InlineKeyboardButton("Convert as Video",callback_data="convert_video")])
  button.append([InlineKeyboardButton("Cancel ❌",callback_data="cancel")])
 
  markup = InlineKeyboardMarkup(button)
  try:
    await m.reply_text(text,quote=True,reply_markup=markup,parse_mode="markdown",disable_web_page_preview=True)
  except Exception as e:
    log.info(str(e))
