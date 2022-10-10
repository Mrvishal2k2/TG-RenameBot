# This file all codes rights reserved by © Spechdie
import logging
import math
import os
import time
import asyncio
from shutil import copyfile

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def progress_for_pyrogram(
    current,
    total,
    ud_type,
    message,
    start
):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = (
            "[{0}{1}] \n<b>◌Progress😉</b>:<code>〘 {2}% 〙</code>\n".format(
                ''.join(["●" for _ in range(math.floor(percentage / 5))]),
                ''.join(["○" for _ in range(20 - math.floor(percentage / 5))]),
                round(percentage, 2),
            )
        )


        tmp = progress + "<b>Done:</b> <code>〘{0}</code><b> of </b><code> {1}〙</code>\n<b>◌Speed🚀</b>:<code>〘 {2}/s 〙</code>\n<b>◌Time Left⏳</b>:<code>〘 {3} 〙</code>\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            # elapsed_time if elapsed_time != '' else "0 s",
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(text=f"{ud_type}\n {tmp}")
        except:
            pass


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return f"{str(round(size, 2))} {Dic_powerN[n]}B"


def TimeFormatter(milliseconds: int) -> str:
    result = ""
    v_m = 0
    remainder = milliseconds
    r_ange_s = {
        "d, ": (24 * 60 * 60 * 1000),
        "h, ": (60 * 60 * 1000),
        "m, ": (60 * 1000),
        "s, ": (1 * 1000),
        "ms ": 1,
    }
    for age, divisor in r_ange_s.items():
        v_m, remainder = divmod(remainder, divisor)
        v_m = int(v_m)
        if v_m != 0:
            result += f" {v_m} {age} "
    return result


################# Other Utils

async def take_screen_shot(video_file, output_directory, ttl):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + \
        "/" + str(time.time()) + ".jpg"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name
    ]
    # width = "90"
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    return out_put_file_name if os.path.lexists(out_put_file_name) else None

async def copy_file(input_file, output_dir):
    output_file = os.path.join(output_dir, f"{str(time.time())}.jpg")
    # https://stackoverflow.com/a/123212/4723940
    copyfile(input_file, output_file)
    return output_file


# below code not used currently will update it's your in further updates...
async def cult_small_video(video_file, out_put_file_name, start_time, end_time):
    file_genertor_command = [
        "ffmpeg",
        "-hide_banner",
        "-i",
        video_file,
        "-ss",
        start_time,
        "-to",
        end_time,
        "-async",
        "1",
        "-strict",
        "-2",
        "-c",
        "copy",
        out_put_file_name,
    ]
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    logger.info(t_response)
    return out_put_file_name
