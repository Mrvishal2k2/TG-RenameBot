'''
RenameBot
© Mrvishal2k2
'''
import logging
import math
import os
import time
import asyncio
from shutil import copyfile

log = logging.getLogger(__name__)


async def progress_for_pyrogram(current: int, total: int, ud_type: str, message, start: float):
    now = time.time()
    diff = now - start
    if diff < 0.1:
        return
    if round(diff % 10.0) != 0 and current != total:
        return

    percentage = current * 100 / total
    speed = current / diff if diff else 0
    elapsed_ms = round(diff) * 1000
    eta_ms = round((total - current) / speed) * 1000 if speed else 0

    filled = math.floor(percentage / 5)
    bar = "●" * filled + "○" * (20 - filled)

    text = (
        f"{ud_type}\n"
        f"`[{bar}]`\n"
        f"**Progress:** `{round(percentage, 1)}%`\n"
        f"**Done:** `{humanbytes(current)}` of `{humanbytes(total)}`\n"
        f"**Speed:** `{humanbytes(speed)}/s`\n"
        f"**ETA:** `{TimeFormatter(eta_ms) or '0s'}`"
    )
    try:
        await message.edit(text=text)
    except Exception:
        pass


def humanbytes(size: float) -> str:
    if not size:
        return "0 B"
    power = 1024
    n = 0
    labels = {0: "B", 1: "KB", 2: "MB", 3: "GB", 4: "TB"}
    while size >= power and n < 4:
        size /= power
        n += 1
    return f"{round(size, 2)} {labels[n]}"


def TimeFormatter(milliseconds: int) -> str:
    parts = []
    for label, divisor in (("d", 86400000), ("h", 3600000), ("m", 60000), ("s", 1000)):
        v, milliseconds = divmod(milliseconds, divisor)
        if v:
            parts.append(f"{v}{label}")
    return " ".join(parts)


async def take_screen_shot(video_file: str, output_dir: str, ttl: int) -> str | None:
    out = os.path.join(output_dir, f"{time.time():.0f}.jpg")
    proc = await asyncio.create_subprocess_exec(
        "ffmpeg", "-ss", str(ttl), "-i", video_file, "-vframes", "1", out,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await proc.communicate()
    return out if os.path.exists(out) else None


def copy_file(src: str, dest_dir: str) -> str:
    dest = os.path.join(dest_dir, f"{time.time():.0f}.jpg")
    copyfile(src, dest)
    return dest
