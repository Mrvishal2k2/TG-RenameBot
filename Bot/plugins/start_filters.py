'''
RenameBot
© Mrvishal2k2
'''
import os
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply, LinkPreviewOptions
from Bot.config import Config
from Bot.messages import Translation

log = logging.getLogger(__name__)


@Client.on_message(filters.command("start") & filters.private)
async def start_msg(c, m):
    markup = None
    if Config.OWNER_USERNAME:
        markup = InlineKeyboardMarkup([[
            InlineKeyboardButton("Owner", url=f"https://t.me/{Config.OWNER_USERNAME}")
        ]])
    await m.reply_text(Translation.START_TEXT, quote=True, reply_markup=markup,
                       link_preview_options=LinkPreviewOptions(is_disabled=True))


@Client.on_message(filters.command("help") & filters.private)
async def help_user(c, m):
    await m.reply_text(Translation.HELP_TEXT, quote=True)


@Client.on_message(filters.command("cancel") & filters.private)
async def cancel_cmd(c, m):
    reply = m.reply_to_message
    if reply and isinstance(reply.reply_markup, ForceReply):
        await reply.delete()
    await m.reply_text(Translation.CANCEL_MSG, quote=True)


@Client.on_message(filters.command("log") & filters.private & filters.user(Config.OWNER_ID))
async def log_msg(c, m):
    if os.path.exists("Log.txt"):
        await m.reply_document("Log.txt", quote=True)
    else:
        await m.reply_text("Log file not found.", quote=True)
