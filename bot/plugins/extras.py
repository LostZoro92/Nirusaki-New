import pymongo, os , pyrogram, time
from bot.database import setffmpeg, getffmpeg, adduser, uploadtype, setmode, uploadtype1
from .devtools import progress_for_pyrogram
from .ffmpeg import functions, ffmpeg
from bot import bot, Config, LOGS


async def changeffmpeg(bot, message):
 try:
    await adduser(message)
    changeffmpeg = message.text.split(" ", maxsplit=1)[1]
    await setffmpeg(message, changeffmpeg)
    print(changeffmpeg)
    await message.reply_text("🗜 **Changed FFmpeg Code.**", quote=True)
 except Exception as e:
    await message.reply_text(f"❗️**Error:** `{e}`", quote=True)


async def changemode(bot, message):
 try:
   newmode = message.text.split(" ", maxsplit=1)[1]
   if "video" == newmode:
    await setmode(message, newmode)
    await bot.send_message(text="🎞️ **Changed Upload Mode.**", chat_id=message.from_user.id, reply_to_message_id=message.id)
   elif "document" == newmode:
    await setmode(message, newmode)
    await bot.send_message(text="📄 **Changed Upload Mode.**", chat_id=message.from_user.id, reply_to_message_id=message.id)
   else:
    await bot.send_message(text="❌ **Unknown Upload Type.**", chat_id=message.from_user.id, reply_to_message_id=message.id)
 except Exception as e:
    await bot.send_message(text=f"❗️**Error:** `{e}`", chat_id=message.from_user.id, reply_to_message_id=message.id)


async def get_type(bot, message):
  upload_type = await uploadtype(message)
  await bot.send_message(text=f"✨ **Your Current Upload Mode Is:**\n`{upload_type}`", chat_id=message.from_user.id, reply_to_message_id=message.id)


async def get_ffmpeg(bot, message):
  ffmpegcodee = await getffmpeg(message)
  print(ffmpegcodee)
  await bot.send_message(text=f"✨ **Your Current FFmpeg Code Is:**\n`{ffmpegcodee}`", chat_id=message.from_user.id, reply_to_message_id=message.id)


async def upload_dir(client, message):
    u_start = time.time()
    if message.reply_to_message:
        message = message.reply_to_message
    cmd1 = message.text.split(" ", maxsplit=1)[1]
    replyid = message.id
    if message.from_user.id in Config.OWNER:
        if os.path.exists(cmd1):
            xhamster = await bot.send_message(text=f"📤 **Uploading File:**", chat_id=message.from_user.id, reply_to_message_id=message.id)
            await client.send_document(
                chat_id=message.chat.id,
                document=cmd1,
                caption=cmd1,
                reply_to_message_id=replyid,
                progress=progress_for_pyrogram,
                progress_args=(client, "📤 **Uploading File:**", xhamster, u_start)
            )
            await xhamster.delete()
        else:
            await bot.send_message(text=f"❌ **File Directory Not Found:**\n`{cmd1}`", chat_id=message.from_user.id, reply_to_message_id=message.id)
    elif Config.TEMP in cmd1:
        if os.path.exists(cmd1):
            xhamster = await bot.send_message(text=f"📤 **Uploading File:**", chat_id=message.from_user.id, reply_to_message_id=message.id)
            await client.send_document(
                chat_id=message.chat.id,
                document=cmd1,
                caption=cmd1,
                reply_to_message_id=replyid,
                progress=progress_for_pyrogram,
                progress_args=(client, "📤 **Uploading File:**", xhamster, u_start)
            )
            await xhamster.delete()
        else:
            await bot.send_message(text=f"❌ **File Directory Not Found:**\n`{cmd1}`", chat_id=message.from_user.id, reply_to_message_id=message.id)
    else:
        await bot.send_message(text=f"🛑 **Access Denied.** You're Not Authorized To Access This Directory.", chat_id=message.from_user.id, reply_to_message_id=message.id)


async def download_dir(bot, message):
 d_start = time.time()
 if message.reply_to_message:
  reply = await bot.send_message(text=f"📥 **Downloading Video:**", chat_id=message.from_user.id, reply_to_message_id=message.id)
  video = await bot.download_media(
        message=message.reply_to_message,
        file_name=Config.TEMP,
        progress=progress_for_pyrogram,
        progress_args=(bot, "📥 **Downloading Video:**", reply, d_start)
  )
  await reply.edit(f"📂 **Directory Is:** `{video}`")
 else:
  await bot.send_message(text=f"⚠️ **Reply To A File To Download It.**", chat_id=message.from_user.id, reply_to_message_id=message.id)


async def sample(bot, message):
 if message.reply_to_message:
   d_start = time.time()
   reply = await bot.send_message(text="📥 **Downloading Video:**", chat_id=message.from_user.id, reply_to_message_id=message.id)
   video = await bot.download_media(
        message=message.reply_to_message,
        file_name=Config.TEMP,
        progress=progress_for_pyrogram,
        progress_args=(bot, "📥 **Downloading Video:**", reply, d_start)
   )
   path , filename = os.path.split(video)
   output_filename = filename + '_sample.mkv'
   await reply.edit("🚀 **Generating Sample...**")
   sample = await functions.sample(filepath=video, output=output_filename)
   caption = filename + " SAMPLE"
   await upload_handle(bot, message, sample, filename, caption, reply)
   os.remove(video)
   os.remove(sample)
   await reply.delete(True)
 else:
  await bot.send_message(text=f"⚠️ **Reply To A File To Download It.**", chat_id=message.from_user.id, reply_to_message_id=message.id)


async def vshots(bot, message):
  if message.reply_to_message:
   cmd1 = int(message.text.split(" ", maxsplit=1)[1])
   if cmd1 > 30:
    return message.reply_text("Bak BSDK")
   d_start = time.time()
   reply = await bot.send_message(text="📥 **Downloading Video:**", chat_id=message.from_user.id, reply_to_message_id=message.id)
   video = await bot.download_media(
        message=message.reply_to_message,
        file_name=Config.TEMP,
        progress=progress_for_pyrogram,
        progress_args=(bot, "📥 **Downloading Video:**", reply, d_start)
   )
   for x in range (1, cmd1):
    ss = await functions.screenshot(filepath=video)
    u_start = time.time()
    await reply.edit(f"🚀 **Starting To Upload The Photo {x}...**")
    await bot.send_photo(chat_id=message.from_user.id,photo=str(ss), caption=x, progress=progress_for_pyrogram, progress_args=(bot, f"📤 **Uploading Photo:**", reply, u_start))
    os.remove(ss)
   os.remove(video)
   reply.delete(True)
  else:
   await message.reply_text("⚠️ **Reply To A File To Download It.**", quote=True)


async def upload_handle(bot, message, filepath, filename, caption, reply):
 try:
  if os.path.exists(filepath) == False:
   return bot.send_message(chat_id=from_user_id, text="❌ **File Not Found Unable To Upload.**")
  mode = await uploadtype(message)
  if mode != "video":
    u_start = time.time()
    thumb = await functions.screenshot(filepath)
    width, height = await ffmpeg.resolution(filepath)
    duration2 = await ffmpeg.duration(filepath)
    s = await bot.send_video(
      video=filepath,
      chat_id=message.from_user.id,
      supports_streaming=True,
      file_name=filename,
      thumb=thumb,
      duration=duration2,
      width=width,
      height=height,
      caption=caption,
      reply_to_message_id=message.id,
      progress=progress_for_pyrogram,
      progress_args=(
        bot,
        "📤 **Uploading Video:**",
        reply,
        u_start
      )
    )
    os.remove(thumb)
  else:
   u_start = time.time()
   thumb = await functions.screenshot(filepath)
   width, height = await ffmpeg.resolution(filepath)
   duration2 = await ffmpeg.duration(filepath)
   s = await bot.send_video(
     video=filepath,
     chat_id=message.from_user.id,
     supports_streaming=True,
     file_name=filename,
     thumb=thumb,
     duration=duration2,
     width=width,
     height=height,
     caption=caption,
     reply_to_message_id=message.id,
     progress=progress_for_pyrogram,
     progress_args=(
       bot,
       "📤 **Uploading Video:**",
       reply,
       u_start
     )
   )
   os.remove(thumb)
 except Exception as e:
  LOGS.info(e)


async def upload_handle1(bot, from_user_id, filepath, filename, caption, reply, reply_to_message):
 mode = await uploadtype1(from_user_id)
 if os.path.exists(filepath) == False:
  return bot.send_message(chat_id=from_user_id, text="❌ **File Not Found Unable To Upload.**")
 if mode == 'document':
  u_start = time.time()
  thumb = await functions.screenshot(filepath)
  s = await bot.send_document(
     document=filepath,
     chat_id=from_user_id,
     force_document=True,
     file_name=filename,
     thumb=thumb,
     reply_to_message_id=reply_to_message,
     progress=progress_for_pyrogram,
     progress_args=(bot, "📤 **Uploading Video:**", reply, u_start)
  )
  os.remove(thumb)
  await s.forward(Config.LOG_CHANNEL)
 elif mode == 'video':
  u_start = time.time()
  thumb = await functions.screenshot(filepath)
  width, height = await ffmpeg.resolution(filepath)
  duration2 = await ffmpeg.duration(filepath)
  caption_text = f"<b>{caption}</b>"
  s = await bot.send_video(
      video=filepath,
      chat_id=from_user_id,
      supports_streaming=True,
      file_name=filename,
      thumb=thumb,
      duration=duration2,
      width=width,
      height=height,
      caption=caption_text,
      reply_to_message_id=reply_to_message,
      progress=progress_for_pyrogram,
      progress_args=(bot, "📤 **Uploading Video:**", reply, u_start)
  )
  os.remove(thumb)
  await s.forward(Config.LOG_CHANNEL)
