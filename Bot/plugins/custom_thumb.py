'''
RenameBot
© Mrvishal2k2
'''
import os
import logging
from pyrogram import Client, filters
from Bot.config import Config
from Bot.messages import Translation
from Bot.utils import save_thumb, delete_thumb, get_thumb

log = logging.getLogger(__name__)

_thumb_path = lambda uid: os.path.join(Config.DOWNLOAD_LOCATION, "thumb", f"{uid}.jpg")


@Client.on_message(filters.photo & filters.private)
async def save_photo(c, m):
    uid = m.from_user.id
    path = _thumb_path(uid)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    await save_thumb(uid, m.id)
    await c.download_media(m, file_name=path)
    await m.reply_text(Translation.THUMB_SAVED_MSG, quote=True)


@Client.on_message(filters.command("deletethumb") & filters.private)
async def delete_thumbnail(c, m):
    uid = m.from_user.id
    path = _thumb_path(uid)
    row = await get_thumb(uid)
    if not row:
        await m.reply_text(Translation.THUMB_NOT_SET_MSG, quote=True)
        return
    await delete_thumb(uid)
    if os.path.exists(path):
        os.remove(path)
    await m.reply_text(Translation.THUMB_DELETED_MSG, quote=True)


@Client.on_message(filters.command("showthumb") & filters.private)
async def show_thumbnail(c, m):
    uid = m.from_user.id
    path = _thumb_path(uid)

    if not os.path.exists(path):
        row = await get_thumb(uid)
        if row:
            try:
                msg = await c.get_messages(m.chat.id, row.msg_id)
                await msg.download(file_name=path)
            except Exception as e:
                log.warning(f"Could not fetch thumb: {e}")
                path = None
        else:
            path = None

    if not path:
        await m.reply_text(Translation.THUMB_NOT_FOUND_MSG, quote=True)
        return

    await m.reply_photo(photo=path, caption=Translation.THUMB_SHOW_CAPTION, quote=True)
