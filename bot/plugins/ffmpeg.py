import pyrogram, asyncio, subprocess, time, os, re, math
from random import randint
from subprocess import Popen
from bot import Config, bot, LOGS
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from html_telegraph_poster import TelegraphPoster


class ffmpeg(object):

 async def duration(filepath):
  try:
   process = subprocess.Popen(
    [
      'ffmpeg',
      "-hide_banner",
      '-i',
      filepath
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
   )
   stdout, stderr = process.communicate()
   output = stdout.decode().strip()
   duration = re.search("Duration:\s*(\d*):(\d*):(\d+\.?\d*)[\s\w*$]",output)
   bitrates = re.search("bitrate:\s*(\d+)[\s\w*$]",output)
   if duration is not None:
     hours = int(duration.group(1))
     minutes = int(duration.group(2))
     seconds = math.floor(float(duration.group(3)))
     total_seconds = ( hours * 60 * 60 ) + ( minutes * 60 ) + seconds
     int_time = int(total_seconds)
   else:
     total_seconds = 25
   return total_seconds
  except Exception as e:
   LOGS.info(e)


 async def resolution(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("width") and metadata.has("height"):
      return metadata.get("width"), metadata.get("height")
    else:
      return 1280, 720


 async def mp4(filepath):
  try:
   output = filepath + '.mp4'
   cmd = f'ffmpeg -loglevel error -i  "{filepath}" -map 0:a -map 0:v -c:a copy -c:v copy "{output}" -y'
   process = await asyncio.create_subprocess_shell(
    cmd,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE
   )
   stdout , stderr = await process.communicate()
   LOGS.info(stdout)
   LOGS.info(stderr)
   return output
  except Exception as e:
   return None


 async def mkv(filepath):
  try:
   output = filepath + '.mkv'
   cmd = f'ffmpeg -i  "{filepath}" -c copy "{output}" -y'
   process = await asyncio.create_subprocess_shell(
    cmd,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE
   )
   stdout , stderr = await process.communicate()
   LOGS.info(stdout)
   LOGS.info(stderr)
   return output
  except Exception as e:
   LOGS.info(e)
   return None


class functions(object):
   def __init__(self):
    self.base__url = "t.me"

   async def mediainfo(filepath):
    try:
     process = subprocess.Popen(
        ["mediainfo", filepath, "--Output=HTML"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
     )
     stdout, stderr = process.communicate()
     out = stdout.decode()
     abc = await bot.get_me()
     name = abc.first_name
     username = abc.username
     client = TelegraphPoster(use_api=True)
     client.create_api_token("Mediainfo")
     page = client.post(
        title="Mediainfo",
        author=name,
        author_url=f"https://t.me/{username}",
        text=out,
     )
     return page["url"]
    except Exception as e:
     LOGS.info(e)
     return "404"


   async def sample(filepath, output):
     try:
      time_latest = time.time()
      output_file = output
      duration = await ffmpeg.duration(filepath=filepath)
      sample_duration = 87
      best_duration = duration - sample_duration
      ss = randint(1, int(best_duration))
      file_gen_cmd = f'ffmpeg -loglevel error -ss {str(ss)} -i "{filepath}" -map 0:v -map 0:a  -c:a copy -c:v copy -t {str(sample_duration)} "{output_file}" -y'
      process = await asyncio.create_subprocess_shell(
        file_gen_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
      )
      stdout, stderr = await process.communicate()
      LOGS.info(stderr)
      return output_file
     except Exception as e:
      return None


   async def screenshot(filepath):
    time_latest = time.time()
    screenshot = f'{time_latest}.jpg'
    duration = await ffmpeg.duration(filepath=filepath)
    ss = randint(2, duration)
    cmd = f'ffmpeg -ss {str(ss)} -i "{filepath}" -vframes 1 "{screenshot}" -y'
    process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    return screenshot
