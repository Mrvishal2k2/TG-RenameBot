'''
RenameBot
© Mrvishal2k2
'''
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LinkPreviewOptions
from Bot.plugins import authorized
from Bot.messages import Translation

log = logging.getLogger(__name__)

_MEDIA_FILTER = (
    filters.document | filters.video | filters.audio
    | filters.voice | filters.video_note | filters.animation
)


@Client.on_message(_MEDIA_FILTER & filters.private & authorized)
async def rename_filter(c, m):
    media = (
        m.document or m.video or m.audio
        or m.voice or m.video_note or m.animation
    )
    name = getattr(media, "file_name", None) or "Unknown"
    text = f"**File:** `{name}`\n\nChoose an action:"

    buttons = [
        [InlineKeyboardButton("📄 Rename as File", callback_data="rename_file"),
         InlineKeyboardButton("🎬 Rename as Video", callback_data="rename_video")],
    ]
    if getattr(media, "mime_type", "").startswith("video/"):
        buttons.append([
            InlineKeyboardButton("📁 Convert to File", callback_data="convert_file"),
            InlineKeyboardButton("▶️ Convert to Video", callback_data="convert_video"),
        ])
    buttons.append([InlineKeyboardButton("❌ Cancel", callback_data="cancel")])

    await m.reply_text(text, quote=True, reply_markup=InlineKeyboardMarkup(buttons),
                       link_preview_options=LinkPreviewOptions(is_disabled=True))
