'''
RenameBot
This file is a part of mrvishal2k2 rename repo 
Dont kang !!!
© Mrvishal2k2
'''

import pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# the Strings used for this "thing"
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

@Client.on_message(filters.document | filters.video | filters.audio | filters.voice | filters.video_note | filters.animation)
async def rename_filter(c,m):
    media = m.document or m.video or m.audio or m.voice or m.video_note or m.animation
    text = ""
    try:
      filename = media.file_name
      text += f"FileName:\n{filename}\n"
    except:
    # some files dont gib name ..
      filename = None 

    text += "Select the desired Option"
    button = [
        [InlineKeyboardButton("Rename as File", callback_data="rename_file")]
    ]
    # Thanks to albert for mime_type suggestion
    if media.mime_type.startswith("video/"):
        button.extend(
            (
                [
                    InlineKeyboardButton(
                        "Rename as Video", callback_data="rename_video"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Convert to File", callback_data="convert_file"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Convert to Video ", callback_data="convert_video"
                    )
                ],
            )
        )
    button.append([InlineKeyboardButton("Cancel ❌",callback_data="cancel")])


    try:
      await m.reply_text(text,quote=True,
         reply_markup=InlineKeyboardMarkup(button),
         disable_web_page_preview=True)
    except Exception as e:
      await m.reply(f"Error\n {e}", True)

      log.error(str(e))
