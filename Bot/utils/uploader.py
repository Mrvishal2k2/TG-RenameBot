'''
RenameBot
© Mrvishal2k2
'''
import os
import time
import random
import asyncio
import logging
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from pyrogram.errors import FloodWait
from pyrogram.types import ReplyParameters
from Bot.config import Config
from Bot.messages import Translation
from Bot.utils.utils import progress_for_pyrogram, copy_file, take_screen_shot

log = logging.getLogger(__name__)

_VIDEO_EXT = (".mkv", ".mp4", ".webm")
_AUDIO_EXT = (".mp3", ".m4a", ".m4b", ".flac", ".wav")


def _thumb_path(user_id: int) -> str:
    return os.path.join(Config.DOWNLOAD_LOCATION, "thumb", f"{user_id}.jpg")


def _resize_thumb(path: str) -> None:
    try:
        img = Image.open(path).convert("RGB")
        w, h = img.size
        new_w = 320
        new_h = int(h * new_w / w) if w else h
        img.resize((new_w, new_h), Image.LANCZOS).save(path, "JPEG")
    except Exception as e:
        log.warning(f"Thumb resize failed: {e}")


def _get_metadata(filepath: str) -> dict:
    try:
        meta = extractMetadata(createParser(filepath))
        if not meta:
            return {}
        result = {}
        if meta.has("duration"):
            result["duration"] = int(meta.get("duration").seconds)
        if meta.has("width"):
            result["width"] = meta.get("width")
        if meta.has("height"):
            result["height"] = meta.get("height")
        if meta.has("title"):
            result["title"] = meta.get("title")
        if meta.has("artist"):
            result["artist"] = meta.get("artist")
        return result
    except Exception:
        return {}


async def _send_with_floodwait(coro_fn, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            return await coro_fn()
        except FloodWait as e:
            wait = e.value
            log.info(f"FloodWait {wait}s (attempt {attempt + 1}/{max_retries})")
            await asyncio.sleep(wait)
        except Exception as e:
            log.error(f"Upload error: {e}")
            raise
    raise RuntimeError("Upload failed after max FloodWait retries")


async def uploader(bot, file: str, update, msg, as_file: bool = False):
    start_time = time.time()
    fname_no_ext = os.path.splitext(os.path.basename(file))[0]
    caption = fname_no_ext
    if Config.CUSTOM_CAPTION:
        caption = f"{fname_no_ext}\n{Config.CUSTOM_CAPTION}"

    user_id = update.from_user.id if update.from_user else update.chat.id
    saved_thumb = _thumb_path(user_id)
    file_dir = os.path.dirname(os.path.abspath(file))
    thumb_copy = None

    if as_file:
        if os.path.exists(saved_thumb):
            thumb_copy = copy_file(saved_thumb, file_dir)

        await _send_with_floodwait(lambda: bot.send_document(
            document=file,
            chat_id=update.chat.id,
            reply_parameters=ReplyParameters(message_id=update.id),
            disable_notification=True,
            disable_content_type_detection=True,
            thumb=thumb_copy,
            caption=caption,
            progress=progress_for_pyrogram,
            progress_args=(Translation.UPLOAD_MSG, msg, start_time),
        ))

    elif file.lower().endswith(_VIDEO_EXT):
        meta = _get_metadata(file)
        duration = meta.get("duration", 0)

        if os.path.exists(saved_thumb):
            thumb_copy = copy_file(saved_thumb, file_dir)
        else:
            ttl = random.randint(0, max(duration - 1, 0))
            thumb_copy = await take_screen_shot(file, file_dir, ttl)

        if thumb_copy and os.path.exists(thumb_copy):
            _resize_thumb(thumb_copy)
            t_meta = _get_metadata(thumb_copy)
            width = t_meta.get("width", meta.get("width", 0))
            height = t_meta.get("height", meta.get("height", 0))
        else:
            width = meta.get("width", 0)
            height = meta.get("height", 0)

        await _send_with_floodwait(lambda: update.reply_video(
            video=file,
            quote=True,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb_copy,
            caption=caption,
            disable_notification=True,
            supports_streaming=True,
            progress=progress_for_pyrogram,
            progress_args=(Translation.UPLOAD_MSG, msg, start_time),
        ))

    elif file.lower().endswith(_AUDIO_EXT):
        meta = _get_metadata(file)
        if os.path.exists(saved_thumb):
            thumb_copy = copy_file(saved_thumb, file_dir)

        await _send_with_floodwait(lambda: update.reply_audio(
            audio=file,
            quote=True,
            thumb=thumb_copy,
            caption=caption,
            duration=meta.get("duration", 0),
            performer=meta.get("artist", ""),
            title=meta.get("title", fname_no_ext),
            disable_notification=True,
            progress=progress_for_pyrogram,
            progress_args=(Translation.UPLOAD_MSG, msg, start_time),
        ))

    else:
        # Unknown extension — fall back to document
        await uploader(bot, file, update, msg, as_file=True)
        return

    if thumb_copy and os.path.exists(thumb_copy):
        os.remove(thumb_copy)
