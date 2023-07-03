import os, asyncio, anitopy, datetime, subprocess, time, pyrogram, math, re, psutil, signal, platform
from bot import LOGS, Config, bot, data, list_handler, queue, words
import json
from pyrogram import Client
from .ffmpeg import functions, ffmpeg
from .devtools import progress_for_pyrogram, progress_for_pyrogram1
from .extras import upload_handle, upload_handle1
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
import re
from psutil import disk_usage, cpu_percent, virtual_memory, Process as psprocess
from bot.database import getffmpeg, getffmpeg1
from pathlib import Path

FINISHED_PROGRESS_STR = "▪️"
UN_FINISHED_PROGRESS_STR = "▫️"


async def ffprobe(i_filepath):
    no_of_subs, no_of_vids, no_of_audios = 0, 0 ,0
    subpath, directory = os.path.split(i_filepath)
    ofp = directory + '.json'
    code = f'ffprobe -v quiet -print_format json -show_format -show_streams "{i_filepath}" > "{directory}.json"'
    process = await asyncio.create_subprocess_shell(code, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout , stderr = await process.communicate()
    if os.path.exists(ofp) == True:
        with open(ofp, 'r') as file:
            stp = file.read()
            bb = json.loads(stp)
            streams = bb["streams"]
            for x  in range(0,len(streams)):
             ld = streams[x]
             if ld["codec_type"] == 'audio':
              no_of_audios = no_of_audios + 1
             if ld["codec_type"] == 'video':
              no_of_vids = no_of_vids + 1
             if ld["codec_type"] == 'subtitle':
              no_of_subs = no_of_subs + 1
        return no_of_subs, no_of_vids, no_of_audios
    else:
     return None, None, None


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "")
    return tmp[:-2]


async def renew(e):
    await e.reply_text("✅ **Cleared Queued, Working Files and Cached Downloads!**", quote=True)
    list_handler.clear()
    data.clear()
    queue.delete_many({})
    os.system("rm downloads/*")
    os.system("rm encodes/*")
    for proc in psutil.process_iter():
        processName = proc.name()
        processID = proc.pid
        if (processName == "ffmpeg"):
         os.kill (processID,signal.SIGKILL)
    return


async def sysinfo(e):
    message = await e.reply_text(
        "🚀 **Getting System Information...**",
        quote=True)
    start_time = time.monotonic()
    last_content = None

    os_info = f"**Operating System:** {platform.system()} {platform.release()} ({platform.machine()})\n\n"
    os_info += "".join(["━"] * 21) + "\n"

    while time.monotonic() - start_time <= 137:
        cpu_usage = psutil.cpu_percent(percpu=True)
        cpu_freq = psutil.cpu_freq()
        cpu_count = psutil.cpu_count(logical=False)
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_count_virtual = cpu_count_logical - cpu_count
        ram_stats = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        dl_size = psutil.net_io_counters().bytes_recv
        ul_size = psutil.net_io_counters().bytes_sent

        cpu_bar = ['⬢' * int(percent / 10) + '⬡' * (10 - int(percent / 10)) for percent in cpu_usage]
        freq_current = f"{round(cpu_freq.current / 1000, 2)} GHz"
        if cpu_freq.min > 0 and cpu_freq.max > 0:
            freq_min = f"{round(cpu_freq.min / 1000, 2)} GHz"
            freq_max = f"{round(cpu_freq.max / 1000, 2)} GHz"
            freq_info = f"**CPU Frequency:** {freq_current} (**Min:** {freq_min}, **Max:** {freq_max})\n\n"
        else:
            freq_info = f"🖥️ **CPU Frequency:** {freq_current}\n\n"

        ram_perc = int(ram_stats.percent)
        ram_used = psutil._common.bytes2human(ram_stats.used)
        ram_total = psutil._common.bytes2human(ram_stats.total)
        ram_bar = '▪️' * int(ram_perc / 10) + '▫️' * (10 - int(ram_perc / 10))
        if ram_perc > 80:
            ram_emoji = "‼️"
        elif ram_perc > 20:
            ram_emoji = "🚀"
        else:
            ram_emoji = "🎮"
        ram_info = f"{ram_emoji} **RAM Usage:** {ram_perc}%\n[{ram_bar}]\n**Used:** {ram_used} **of** {ram_total}\n**Free :**  {psutil._common.bytes2human(ram_stats.available)}\n"

        disk_perc = int(disk.percent)
        disk_used = psutil._common.bytes2human(disk.used)
        disk_total = psutil._common.bytes2human(disk.total)
        disk_bar = '▪️' * int(disk_perc / 10) + '▫️' * (10 - int(disk_perc / 10))
        disk_info = f"💾 **Disk Usage:** {disk_perc}%\n[{disk_bar}]\n**Used:** {disk_used} **of** {disk_total}\n**Free :**  {psutil._common.bytes2human(disk.free)}\n"

        sys_info = f"{os_info}{freq_info}"
        for i, percent in enumerate(cpu_usage[:cpu_count]):
            if cpu_count > 9 and i < 9:
                core_num = f"0{i+1}"
            else:
                core_num = str(i+1)
            sys_info += f"[{cpu_bar[i]}] **Core {core_num}:** {percent:.1f}%\n"
        sys_info += f"\n\t◉ **Physical Cores:** {cpu_count}\n"
        if cpu_count_virtual > 0:
            sys_info += f"\t◉ **Logical Cores:** {cpu_count_virtual}\n"
        else:
            sys_info += ""
        sys_info += "".join(["━"] * 21) + "\n"
        sys_info += ram_info
        sys_info += "".join(["━"] * 21) + "\n"
        sys_info += disk_info
        sys_info += "".join(["━"] * 21) + "\n"
        sys_info += f"🔻 **DL :** {psutil._common.bytes2human(dl_size)} **|** 🔺 **UL :** {psutil._common.bytes2human(ul_size)}"

        if sys_info != last_content:
            await message.edit_text(sys_info)
            last_content = sys_info

        await asyncio.sleep(3)

    await message.edit_text("🎯 **Time Limit Reached!**")


def hbs(size):
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "B", 1: "K", 2: "M", 3: "G", 4: "T", 5: "P"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


@bot.on_callback_query()

async def stats(bot: Client, event: CallbackQuery):
 try:
  if "stats" == event.data:
   data = os.listdir("encodes/")
   down = os.listdir("downloads/")
   i_file = f'downloads/{down[0]}'
   file = f'encodes/{data[0]}'
   op = hbs(int(Path(i_file).stat().st_size))
   ot = hbs(int(Path(file).stat().st_size))
   ans = f"Original: {down[0]}\n\nFile Size: {op}\n\n\nEncoded: {data[0]}\n\nFile Size: {ot}"
   await event.answer(ans, show_alert=True)
  elif "cancel" == event.data:
   for proc in psutil.process_iter():
    processName = proc.name()
    processID = proc.pid
    if processName == "ffmpeg":
     os.kill(processID, signal.SIGKILL)
   await event.answer("Process Killed ☠️", show_alert=True)
 except Exception as e:
   await event.answer("✖️ Error 404: File | Info not Found,\nKindly Resend Media.", show_alert=True)
   LOGS.info(e)


async def encode_it(input_file, output, message, obj, total_time):
   extra = await getffmpeg1(obj)
   code = f'ffmpeg -progress progress.txt -loglevel error -i "{input_file}" {extra} -y "{output}"'
   process = await asyncio.create_subprocess_shell(
        code,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
   COMPRESSION_START_TIME = time.time()
   while process.returncode != 0:
    try:
     await asyncio.sleep(3)
     with open("progress.txt", 'r+') as file:
        text = file.read()
        frame = re.findall("frame=(\d+)", text)
        time_in_us=re.findall("out_time_ms=(\d+)", text)
        progress=re.findall("progress=(\w+)", text)
        speed=re.findall("speed=(\d+\.?\d*)", text)
        if len(frame):
          frame = int(frame[-1])
        else:
          frame = 1;
        if len(speed):
          speed = speed[-1]
        else:
          speed = 1;
        if len(time_in_us):
          time_in_us = time_in_us[-1]
        else:
          time_in_us = 1;
        if len(progress):
          if progress[-1] == "end":
            break
        execution_time = TimeFormatter((time.time() - COMPRESSION_START_TIME)*1000)
        dpcd = os.listdir("encodes/")
        fis = f'encodes/{dpcd[0]}'
        ottt = hbs(int(Path(fis).stat().st_size))
        elapsed_time = int(time_in_us)/1000000
        difference = math.floor((total_time - elapsed_time) / float(speed))
        ETA = "-"
        if difference > 0:
          ETA = TimeFormatter(difference*1000)
        percentage = math.floor(elapsed_time * 100 / total_time)
        perc_str = '{0}%'.format(round(percentage, 2))
        prog_bar_str = '{0}{1}'.format(''.join([FINISHED_PROGRESS_STR for i in range(math.floor(percentage / 10))]), ''.join([UN_FINISHED_PROGRESS_STR for i in range(10 - math.floor(percentage / 10))]))
        stats = f'🗜 **Compressing Video:**' \
                f' {perc_str}\n' \
                f'[{prog_bar_str}]\n' \
                f'**Encoded:** {ottt}\n\n' \
                f'◉ **Time Left:** {ETA}'
        try:
          await message.edit(text=stats, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data=f"cancel"), InlineKeyboardButton("FILE STATUS", callback_data=f"stats")]]))
        except Exception as e:
          cast = None
          for proc in psutil.process_iter():
           processName = proc.name()
           if (processName == "ffmpeg"):
            cast = True
          if cast == True:
            continue
          else:
            break
    except Exception as e:
      break
   stdout, stderr = await process.communicate()
   LOGS.info(stderr)


def removeUsernames(string):
    st = re.sub(r'\.?@(\w+)\s*', '', string)
    st = re.sub(r'\([^)]*\)', '', st)
    st = re.sub(r'\s{2,}|-', ' ', st.strip())
    return st

def removeLeadingZeros(string):
    regex = "^0+(?!$)"
    st = re.sub(regex, "", string)
    return st

async def parser(name):
   string = ''
   dic = anitopy.parse(name)
   if 'anime_season' in dic.keys():
    season = dic['anime_season']
    season = removeLeadingZeros(str(season))
    string = f'{season}×'
   if 'episode_number' in dic.keys():
    ep = str(dic['episode_number'])
    string = string + f'{ep} - '
   if 'anime_title' in dic.keys():
     anime = dic['anime_title']
     anime = removeUsernames(str(anime))
     string = string + f'{anime}'
   else:
    anime = ''
   return string


async def download_video(download, reply):
 d_start =  time.time()
 video = await bot.download_media(
        message=download,
        file_name=Config.DOWNLOAD_DIR,
        progress=progress_for_pyrogram,
        progress_args=(bot, "📥 **Downloading Video:**", reply, d_start)
      )
 return video


async def replacee(filename):
    b = words.find({})
    dbc = []
    for bc in b:
     dbc.append(bc["word"])
    for c in range(0, len(dbc)):
      if str(dbc[c]) in filename:
        filename = filename.replace(str(dbc[c]), '')
    return filename


async def mediainfo(app, message):
  if message.reply_to_message:
   video = message.reply_to_message.id
   msg = await app.send_message(chat_id=message.chat.id, reply_to_message_id=message.reply_to_message.id, text="📥 **Downloading Video:**", disable_web_page_preview=True)
   d_start = time.time()
   filepath = await app.download_media(
        message=message.reply_to_message,
        file_name=Config.DOWNLOAD_DIR,
        progress=progress_for_pyrogram,
        progress_args=(
          app,
          "📥 **Downloading Video:**",
          msg,
          d_start
        )
      )
   await msg.edit("🚀 **Getting Mediainfo...**")
   mediainfo = await functions.mediainfo(filepath)
   await msg.edit(f"[Mediainfo]({mediainfo})")
   os.remove(filepath)
  else:
   await app.send_message(message.chat.id, "⚠️ **Reply To A File To Download It.**", reply_to_message_id=message.id)


async def encode(dic):
 try:
  from_user_id = int(dic['from_user']['id'])
  reply_video_id = int(dic['id'])
  dfix = "📥 **Downloading Video:**"
  reply = await bot.send_message(text=dfix, chat_id=from_user_id, reply_to_message_id=reply_video_id)
  media_type = str(dic['media'])
  if media_type == "MessageMediaType.VIDEO":
    file_id = str(dic['video']['file_id'])
    filename = str(dic['video']['file_name'])
    filesize = int(dic['video']['file_size'])
    file_dir = 'downloads/' + filename
  else:
    file_id = str(dic['document']['file_id'])
    filename = str(dic['document']['file_name'])
    filesize = int(dic['document']['file_size'])
    file_dir = 'downloads/' + filename
  d_start = time.time()
  down = await bot.download_media(
     message=file_id,
     file_name=file_dir,
     progress=progress_for_pyrogram1,
     progress_args=(bot, dfix, reply, d_start, filesize)
  )
  filename = await replacee(filename)
  joined = await parser(filename)
  with_ext = joined + '.mkv'
  duration = await ffmpeg.duration(filepath=down)
  output_name = 'encodes/' + joined + '.mkv'
  await encode_it(down, output_name, reply, from_user_id, duration)
  await reply.edit("📤 **Uploading Video:**")
  await upload_handle1(bot, from_user_id, output_name, with_ext, joined, reply, reply_video_id)
  await reply.delete(True)
  os.remove(down)
  os.remove(output_name)
 except Exception as e:
  LOGS.info(e)
