import os
from bot import data, LOGS, list_handler, queue
from bot.plugins.compress import encode
from pyrogram.types import Message


async def add_task1(m):
    try:
        await encode(m)
    except Exception as e:
        LOGS.info(e)
    await on_task_complete()


async def on_task_complete():
    del data[0]
    queue.delete_one({"_id" : list_handler[0]})
    del list_handler[0]
    if len(data) > 0:
      try:
        os.system('rm encodes/*')
      except Exception as e:
        pass
      await add_task1(data[0])
    else:
     data.clear()
     list_handler.clear()
     queue.delete_many({})
