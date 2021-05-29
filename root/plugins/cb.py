'''
RenameBot
This file is a part of mrvishal2k2 rename repo 
Dont kang !!!
© Mrvishal2k2
'''
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup,ForceReply
from root.utils.utils import *
from root.utils.uploader import uploader
import asyncio
from root.messages import Translation
from root.config import Config
from root.utils.database import *
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

@Client.on_callback_query(filters.create(lambda _, __, query: query.data.startswith("rename")))
async def rename_call(c,m):
  if m.data=="rename_file":
    mode = "File"
  elif m.data == "rename_video":
    mode = "Video"
  else: # this couldnt happen
    pass
  await m.message.delete()
  await c.send_message(
    text=f"Mode: {mode} \nNow send me new file name without extension",
    chat_id=m.message.chat.id,
    reply_to_message_id=m.message.reply_to_message.message_id,
    reply_markup=ForceReply(True)
    )

@Client.on_message(filters.private & filters.reply & filters.text)
async def rep_rename_call(c, m):
    # check which mode first
    try:
        get_mode = str(m.reply_to_message.text).splitlines()[0].split(" ")[1]
    except IndexError:
        get_mode = "Video"
    if (m.reply_to_message.reply_markup) and isinstance(m.reply_to_message.reply_markup, ForceReply):
      if get_mode == "File":
        asyncio.create_task(renamer(c, m,as_file=True))   
      else:
        asyncio.create_task(renamer(c, m))
    else:
        print('No media present')


async def renamer(c,m,as_file=False):
  ## 
  bot_msg = await c.get_messages(m.chat.id, m.reply_to_message.message_id) 
  todown = bot_msg.reply_to_message # msg with media
  new_f_name = m.text # new name
  media = todown.document or todown.video or todown.audio or todown.voice or todown.video_note or todown.animation
  try:
    media_name = media.file_name
    extension = media_name.split(".",1)[-1]
  except:
    extension = "mkv"
  await bot_msg.delete() # delete name asked msg 
  if len(new_f_name) > 64:
      await m.reply_text(text=f"Limits of telegram file name is 64 charecters only\nReduce some and try again.")
      return
  d_msg = await m.reply_text(Translation.DOWNLOAD_MSG,True)
  d_location = Config.DOWNLOAD_LOCATION + "/" + str(m.chat.id) + "/"
  d_time = time.time()
  try:
    downloaded_file = await c.download_media(
      message=todown,
      file_name=d_location,
      progress=progress_for_pyrogram,
      progress_args=(
                Translation.DOWNLOAD_MSG,
                d_msg,
                d_time
            )
      )
  except ValueError:
      downloaded_file = None
  except Exception as e:
    log.info(str(e))
  if downloaded_file is None:
    await d_msg.edit_text(Translation.DOWNLOAD_FAIL_MSG)
    return
  new_file_name = d_location + new_f_name + "." + extension
  os.rename(downloaded_file,new_file_name)
  try:
    await d_msg.delete()
    u_msg = await m.reply_text(Translation.UPLOAD_MSG,quote=True)
  except:  # whatever the error but still i need this message to upload 
    u_msg = await m.reply_text(Translation.UPLOAD_MSG,quote=True)
  # try to get thumb to use for later upload
  thumb_image_path = Config.DOWNLOAD_LOCATION + "/thumb/" + str(m.from_user.id) + ".jpg"
  if not os.path.exists(thumb_image_path):
      mes = await thumb(m.from_user.id)
      if mes is not None:
          mesg = await c.get_messages(m.chat.id, mes.msg_id)
          await mesg.download(file_name=thumb_image_path)

  # now need to upload 
  try:
     if as_file:
       await uploader(c,new_file_name,m,u_msg,as_file=True)
     else:
       await uploader(c,new_file_name,m,u_msg)
  except Exception as er:
     await u_msg.edit_text(Translation.UPLOAD_FAIL_MSG)
     log.info(str(er))
     return

  await u_msg.delete()
  if os.path.exists(downloaded_file):
       os.remove(downloaded_file)
  await m.reply_text(Translation.UPLOAD_DONE_MSG,quote=True)
  
  

@Client.on_callback_query(filters.create(lambda _, __, query: query.data.startswith("cancel")))
async def cancel_call(c,m):
   if m.data=="cancel":
      await m.message.delete()
   else:  # I think I need to delete both also in some case currently not used
      await m.message.reply_to_message.delete()
      await m.message.delete()



@Client.on_callback_query(filters.create(lambda _, __, query: query.data.startswith("convert")))
async def convert_call(c,m):
  usr_msg = m.message.reply_to_message
  d_msg = await m.message.edit_text(Translation.DOWNLOAD_MSG)
  d_location = Config.DOWNLOAD_LOCATION + "/" + str(m.from_user.id) + "/"
  d_time = time.time()
  try:
    downloaded_file = await c.download_media(
      message=usr_msg,
      file_name=d_location,
      progress=progress_for_pyrogram,
      progress_args=(
                Translation.DOWNLOAD_MSG,
                d_msg,
                d_time
            )
      )
  except ValueError:
      downloaded_file = None
  except Exception as e:
    log.info(str(e))
  if downloaded_file is None:
    await d_msg.edit_text(Translation.DOWNLOAD_FAIL_MSG)
    return
  try:
    await d_msg.delete()
    u_msg = await usr_msg.reply_text(Translation.UPLOAD_MSG,quote=True)
  except:  # whatever the error but still i need this message to upload 
    u_msg = await usr_msg.reply_text(Translation.UPLOAD_MSG,quote=True)
  # try to get thumb to use later while uploading..
  thumb_image_path = Config.DOWNLOAD_LOCATION + "/thumb/" + str(m.from_user.id) + ".jpg"
  if not os.path.exists(thumb_image_path):
      mes = await thumb(m.from_user.id)
      if mes is not None:
          mesg = await c.get_messages(m.message.chat.id, mes.msg_id)
          await mesg.download(file_name=thumb_image_path)

  # now need to upload 
  try:
     if m.data=="convert_file":
       await uploader(c,downloaded_file,usr_msg,u_msg,as_file=True)
     else:
       await uploader(c,downloaded_file,usr_msg,u_msg)
  except Exception as er:
    await u_msg.edit_text(Translation.UPLOAD_FAIL_MSG)
    log.info(str(er))
    return
  await u_msg.delete()
  if os.path.exists(downloaded_file):
     os.remove(downloaded_file)
  await usr_msg.reply_text(Translation.UPLOAD_DONE_MSG,quote=True)
