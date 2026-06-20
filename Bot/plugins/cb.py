'''
RenameBot
© Mrvishal2k2
'''
import os
import time
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import ForceReply, InlineKeyboardMarkup, InlineKeyboardButton, ReplyParameters
from Bot.config import Config
from Bot.messages import Translation
from Bot.utils import progress_for_pyrogram, get_thumb, uploader

_active_tasks: dict[int, asyncio.Task] = {}

def _cancel_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel_download")]])

log = logging.getLogger(__name__)


async def _ensure_thumb(c, chat_id: int, user_id: int) -> None:
    """Download saved thumb from Telegram to disk if not already cached."""
    path = os.path.join(Config.DOWNLOAD_LOCATION, "thumb", f"{user_id}.jpg")
    if os.path.exists(path):
        return
    row = await get_thumb(user_id)
    if row:
        try:
            msg = await c.get_messages(chat_id, row.msg_id)
            await msg.download(file_name=path)
        except Exception as e:
            log.warning(f"Could not fetch saved thumb: {e}")


# ─── Rename flow ─────────────────────────────────────────────────────────────

@Client.on_callback_query(filters.create(lambda _, __, q: q.data.startswith("rename")))
async def rename_call(c, m):
    mode = "File" if m.data == "rename_file" else "Video"
    await m.message.delete()
    await c.send_message(
        chat_id=m.message.chat.id,
        text=f"Mode: {mode}\n{Translation.SEND_NEW_NAME}",
        reply_parameters=ReplyParameters(message_id=m.message.reply_to_message.id),
        reply_markup=ForceReply(selective=True),
    )


@Client.on_message(filters.private & filters.reply & filters.text)
async def rep_rename_call(c, m):
    reply = m.reply_to_message
    if not (reply and isinstance(reply.reply_markup, ForceReply)):
        return
    try:
        mode = reply.text.splitlines()[0].split(" ")[1]
    except (IndexError, AttributeError):
        mode = "Video"
    task = asyncio.create_task(renamer(c, m, as_file=(mode == "File")))
    _active_tasks[m.from_user.id] = task


async def renamer(c, m, as_file: bool = False):
    uid = m.from_user.id
    bot_msg = await c.get_messages(m.chat.id, m.reply_to_message.id)
    orig = bot_msg.reply_to_message
    new_name = m.text.strip()

    media = (
        orig.document or orig.video or orig.audio
        or orig.voice or orig.video_note or orig.animation
    )
    try:
        extension = media.file_name.rsplit(".", 1)[-1]
    except Exception:
        extension = "mkv"

    await bot_msg.delete()

    if len(new_name) > 64:
        await m.reply_text(Translation.FILENAME_TOO_LONG, quote=True)
        _active_tasks.pop(uid, None)
        return

    d_msg = await m.reply_text(Translation.DOWNLOAD_MSG, quote=True,
                                reply_markup=_cancel_button())
    d_dir = os.path.join(Config.DOWNLOAD_LOCATION, str(uid))
    os.makedirs(d_dir, exist_ok=True)
    downloaded = None

    try:
        downloaded = await c.download_media(
            message=orig,
            file_name=d_dir + "/",
            progress=progress_for_pyrogram,
            progress_args=(Translation.DOWNLOAD_MSG, d_msg, time.time()),
        )
    except asyncio.CancelledError:
        if downloaded and os.path.exists(downloaded):
            os.remove(downloaded)
        try:
            await d_msg.edit_text("❌ Cancelled.")
        except Exception:
            pass
        return
    except Exception as e:
        log.error(f"Download error: {e}")
        await d_msg.edit_text(Translation.DOWNLOAD_FAIL_MSG)
        _active_tasks.pop(uid, None)
        return

    if not downloaded:
        await d_msg.edit_text(Translation.DOWNLOAD_FAIL_MSG)
        _active_tasks.pop(uid, None)
        return

    new_path = os.path.join(d_dir, f"{new_name}.{extension}")
    os.rename(downloaded, new_path)

    await _ensure_thumb(c, m.chat.id, uid)

    try:
        await d_msg.delete()
    except Exception:
        pass
    u_msg = await m.reply_text(Translation.UPLOAD_MSG, quote=True,
                                reply_markup=_cancel_button())

    try:
        await uploader(c, new_path, m, u_msg, as_file=as_file)
    except asyncio.CancelledError:
        if os.path.exists(new_path):
            os.remove(new_path)
        try:
            await u_msg.edit_text("❌ Cancelled.")
        except Exception:
            pass
        return
    except Exception as e:
        log.error(f"Upload error: {e}")
        await u_msg.edit_text(Translation.UPLOAD_FAIL_MSG)
        _active_tasks.pop(uid, None)
        return

    _active_tasks.pop(uid, None)
    await u_msg.delete()
    if os.path.exists(new_path):
        os.remove(new_path)
    await m.reply_text(Translation.UPLOAD_DONE_MSG, quote=True)


# ─── Convert flow ─────────────────────────────────────────────────────────────

@Client.on_callback_query(filters.create(lambda _, __, q: q.data.startswith("convert")))
async def convert_call(c, m):
    uid = m.from_user.id
    orig = m.message.reply_to_message
    d_msg = await m.message.edit_text(Translation.DOWNLOAD_MSG,
                                       reply_markup=_cancel_button())
    d_dir = os.path.join(Config.DOWNLOAD_LOCATION, str(uid))
    os.makedirs(d_dir, exist_ok=True)
    downloaded = None

    task = asyncio.current_task()
    _active_tasks[uid] = task

    try:
        downloaded = await c.download_media(
            message=orig,
            file_name=d_dir + "/",
            progress=progress_for_pyrogram,
            progress_args=(Translation.DOWNLOAD_MSG, d_msg, time.time()),
        )
    except asyncio.CancelledError:
        if downloaded and os.path.exists(downloaded):
            os.remove(downloaded)
        try:
            await d_msg.edit_text("❌ Cancelled.")
        except Exception:
            pass
        return
    except Exception as e:
        log.error(f"Download error: {e}")
        await d_msg.edit_text(Translation.DOWNLOAD_FAIL_MSG)
        _active_tasks.pop(uid, None)
        return

    if not downloaded:
        await d_msg.edit_text(Translation.DOWNLOAD_FAIL_MSG)
        _active_tasks.pop(uid, None)
        return

    await _ensure_thumb(c, m.message.chat.id, uid)

    try:
        await d_msg.delete()
    except Exception:
        pass
    u_msg = await orig.reply_text(Translation.UPLOAD_MSG, quote=True,
                                   reply_markup=_cancel_button())
    as_file = m.data == "convert_file"

    try:
        await uploader(c, downloaded, orig, u_msg, as_file=as_file)
    except asyncio.CancelledError:
        if os.path.exists(downloaded):
            os.remove(downloaded)
        try:
            await u_msg.edit_text("❌ Cancelled.")
        except Exception:
            pass
        return
    except Exception as e:
        log.error(f"Upload error: {e}")
        await u_msg.edit_text(Translation.UPLOAD_FAIL_MSG)
        _active_tasks.pop(uid, None)
        return

    _active_tasks.pop(uid, None)
    await u_msg.delete()
    if os.path.exists(downloaded):
        os.remove(downloaded)
    await orig.reply_text(Translation.UPLOAD_DONE_MSG, quote=True)


# ─── Cancel ──────────────────────────────────────────────────────────────────

@Client.on_callback_query(filters.create(lambda _, __, q: q.data == "cancel"))
async def cancel_call(c, m):
    await m.message.delete()


@Client.on_callback_query(filters.create(lambda _, __, q: q.data == "cancel_download"))
async def cancel_download_call(c, m):
    uid = m.from_user.id
    task = _active_tasks.pop(uid, None)
    if task and not task.done():
        task.cancel()
        await m.answer("Cancelling…")
    else:
        await m.answer("Nothing to cancel.")
