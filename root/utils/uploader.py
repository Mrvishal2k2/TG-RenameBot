'''
© Mrvishal2k2
RenameBot
This file is a part of mrvishal2k2 rename repo 
Dont kang !!!
© Mrvishal2k2
'''
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

import asyncio
import pyrogram
import os
import time
import requests
import shutil
import random
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from root.utils.utils import progress_for_pyrogram, humanbytes, take_screen_shot, copy_file
from root.config import Config
from root.messages import Translation
from pyrogram.errors  import FloodWait

async def uploader(bot,file, update, msg,as_file=False):

    start_time = time.time() 
    afilename = file.split("/")[-1]
    filename = " ".join(afilename.split(".")[0:-1])
    if Config.CUSTOM_CAPTION:
         filename = filename + "\n" + Config.CUSTOM_CAPTION
    # Thumb Location parameter 
    thumb_location = Config.DOWNLOAD_LOCATION + "/thumb/" + str(update.chat.id) + ".jpg" 
    thumb_image_path = None
    if as_file:
        if os.path.exists(thumb_location):
           thumb_image_path = await copy_file(thumb_location, os.path.dirname(os.path.abspath(file)))
        try:
           await bot.send_document(
               document=file,
               chat_id=update.chat.id,
               reply_to_message_id=update.message_id,
               disable_notification=True,
               force_document=True,
               thumb=thumb_image_path,
               progress=progress_for_pyrogram,
               caption=filename,
               progress_args=(
        	      	     Translation.UPLOAD_MSG,
        	      	     msg,
        	      	     start_time
        	      	     ))
        except FloodWait as e:
            logger.info(f"Got Flood Wait of {e.x} second me sleeping now...")
            await asyncio.sleep(e.x)
        except Exception as er:
            logger.info(str(er))
        if thumb_image_path is not None:
             os.remove(thumb_image_path)  
        
    else:
         if file.lower().endswith(("mkv","mp4","webm")):
             # for thumb..
             metadata = extractMetadata(createParser(file))
             duration = 0
             if metadata.has("duration"):
                 duration = metadata.get('duration').seconds
             width = 0
             height = 0
         
             if os.path.exists(thumb_location):
                 thumb_image_path = await copy_file(thumb_location, os.path.dirname(os.path.abspath(file)))
             else:
                 thumb_image_path = await take_screen_shot(file, os.path.dirname(os.path.abspath(file)), random.randint(0, duration - 1))
             
             
             if thumb_image_path is not None:
                 metadata = extractMetadata(createParser(thumb_image_path))
                 if metadata.has("width"):
                      width = metadata.get("width")
                 if metadata.has("height"):
                       height = metadata.get("height")
                 Image.open(thumb_image_path).convert(
                       "RGB"
                     ).save(thumb_image_path)
                 img = Image.open(thumb_image_path)
                 img.resize((320, height))
                 img.save(thumb_image_path, "JPEG")
         
             # upload video..
             try:
                await update.reply_video(
         	  video=file,
         	  quote=True,
         	  duration=duration,
         	  width=width,
         	  height=height,
         	  thumb=thumb_image_path,
                  disable_notification=True,
                  caption=filename,
         	  supports_streaming=True,
         	  progress=progress_for_pyrogram,
                  progress_args=(
        	         Translation.UPLOAD_MSG,
        	   	     msg,
     	      	     start_time
        	   	     ))
             except FloodWait as e:
                 logger.info(f"Got Flood wait of {e.x} seconds ")
                 await asyncio.sleep(e.x)
             except Exception as er:
                  logger.info(str(er))

             if thumb_image_path is not None:
                os.remove(thumb_image_path)  
         
         elif file.lower().endswith(("mp3", "m4a", "m4b", "flac", "wav")):
            metadata = extractMetadata(createParser(file)) 
            duration = 0
            title = ""
            artist = ""
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            if metadata.has("title"):
                title = metadata.get("title")
            if metadata.has("artist"):
                artist = metadata.get("artist")
            
            if os.path.exists(thumb_location):
        	    thumb_image_path = await copy_file(thumb_location, os.path.dirname(os.path.abspath(file)))
         
        # upload now
            try:
               await update.reply_audio(
        	    audio=file,
                 quote=True,
                 thumb=thumb_image_path,
           	    caption=filename,
           	    duration=duration,
           	    performer=artist,
           	    title=title,
                    disable_notification=True,
           	    progress=progress_for_pyrogram,
           	    progress_args=(
        	      	     Translation.UPLOAD_MSG,
        	      	     msg,
        	      	     start_time
        	      	     ))
            except FloodWait as e:
                logger.info("Got Floodwait of {e.x} seconds so me sleeping ")
                await asyncio.sleep(e.x)
            except Exception as er:
                logger.info(str(er))
            if thumb_image_path is not None:
                os.remove(thumb_image_path)  
        
         else:
            if os.path.exists(thumb_location):
              	thumb_image_path = await copy_file(thumb_location, os.path.dirname(os.path.abspath(file)))
            try:
               await update.reply_document(document=file,
        	   quote=True,
        	   thumb=thumb_image_path,
                   progress=progress_for_pyrogram,
                   caption=filename,
                   disable_notification=True,
                   progress_args=(
        	      	     Translation.UPLOAD_MSG,
        	      	     msg,
        	      	     start_time
        	      	     ))
            except FloodWait as e:
                logger.info(f"Got Flood wait of {e.x} seconds Byee mr sleeping ...")
                await asyncio.sleep(e.x)
            except Exception as er:
                logger.info(str(er))
            if thumb_image_path is not None:
                 os.remove(thumb_image_path)  

