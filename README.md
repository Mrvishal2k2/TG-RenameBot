# TG-RenameBot

A Telegram bot to rename/convert media files, written in [Python 3](https://www.python.org) using [Pyrogram](https://docs.pyrogram.org).

Send any file → pick an action via inline buttons (rename as file/video, convert between file and video) → bot downloads, renames or remuxes, and re-uploads with your saved custom thumbnail.

## Requirements

- Python 3.10+
- ffmpeg installed on the system
- PostgreSQL database

## Installation (VPS)

```bash
git clone https://github.com/mrvishal2k2/TG-RenameBot
cd TG-RenameBot
pip install -r requirements.txt
# set environment variables (see below)
python3 bot.py
```

## Docker

```bash
docker build -t tg-renamebot .
docker run --env-file .env tg-renamebot
```

Copy `.env.example` to `.env` and fill in your values.

## Environment Variables

**Required:**

| Variable | Description |
|---|---|
| `APP_ID` | Telegram API ID from [my.telegram.org](https://my.telegram.org/apps) |
| `API_HASH` | Telegram API hash from [my.telegram.org](https://my.telegram.org/apps) |
| `TG_BOT_TOKEN` | Bot token from [@BotFather](https://t.me/BotFather) |
| `OWNER_ID` | Space-separated user IDs with admin access |
| `DATABASE_URL` | PostgreSQL connection URI |

**Optional:**

| Variable | Default | Description |
|---|---|---|
| `AUTH_USERS` | _(everyone)_ | Space-separated user IDs allowed to use the bot |
| `DOWNLOAD_LOCATION` | `./Bot/DOWNLOADS` | Local path for temporary downloads |
| `OWNER_USERNAME` | | Owner's Telegram username (without @) |
| `CUSTOM_CAPTION` | | Text appended to file captions after the filename |

## Commands

```
/start        - start the bot
/help         - usage instructions
/showthumb    - show your saved custom thumbnail
/deletethumb  - delete your saved custom thumbnail
/log          - (owner only) get the log file
```

## Developer

- Telegram: [Mrvishal2k2](https://t.me/Mrvishal_2k2)
- Channel: [BotDunia](https://t.me/BotDunia)

<a href="https://t.me/BotDunia"><img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"></a>
<a href="https://github.com/Mrvishal2k2"><img src="https://img.shields.io/badge/GitHub-Follow%20on%20GitHub-inactive.svg?logo=github"></a>

## Contributing

Pull requests are welcome. Keep deployment simple and newbie-friendly.
