'''
RenameBot
© Mrvishal2k2
'''


class Translation:
    START_TEXT = (
        "👋 **Hi! I'm a Rename & Convert Bot.**\n\n"
        "Send me any media file and I'll let you:\n"
        "• Rename it as a **Document** or **Video**\n"
        "• Convert between Document and Video\n\n"
        "Use /help for full instructions."
    )
    HELP_TEXT = (
        "**How to use:**\n\n"
        "1. Send any file, video, audio, or animation\n"
        "2. Choose an action from the buttons\n"
        "3. For rename → type the new filename (no extension)\n"
        "   Use /cancel to abort a pending rename prompt\n\n"
        "**Thumbnail commands:**\n"
        "• Send a photo → saved as your custom thumbnail\n"
        "• /savethumb — save last sent photo as thumbnail\n"
        "• /showthumb — preview your saved thumbnail\n"
        "• /deletethumb — remove your saved thumbnail\n\n"
        "**Max filename length:** 64 characters"
    )
    WAIT_MSG = "⏳ **Please wait…**"
    DOWNLOAD_MSG = "📥 **Downloading…**"
    DOWNLOAD_FAIL_MSG = "❌ **Download failed.** Please try again."
    UPLOAD_MSG = "📤 **Uploading…**"
    UPLOAD_FAIL_MSG = "❌ **Upload failed.** Please try again."
    UPLOAD_DONE_MSG = "✅ **Upload Done!**"
    THUMB_SAVED_MSG = "✅ Thumbnail saved!"
    THUMB_DELETED_MSG = "🗑 Thumbnail removed."
    THUMB_NOT_FOUND_MSG = "ℹ️ No saved thumbnail found."
    THUMB_SHOW_CAPTION = "Your saved thumbnail.\nUse /deletethumb to remove it."
    FILENAME_TOO_LONG = (
        "❌ Filename too long.\n"
        "Telegram allows max **64 characters**.\n"
        "Please shorten and try again."
    )
    SEND_NEW_NAME = "✏️ **Send me the new filename** (without extension):"
    AUTH_FAIL = "⛔ You are not authorised to use this bot."
    CANCEL_MSG = "✅ Cancelled."
    THUMB_NOT_SET_MSG = "ℹ️ You have no saved thumbnail to delete."
