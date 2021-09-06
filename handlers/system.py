import sys
import shutil
import psutil
import logging
import re
import os
import time
from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime as kek
from helpers.functions import humanbytes, human_readable_bytes, get_readable_time, botStartTime 
from config import BOT_USERNAME, BOT_NAME, SUDO_USERS
from speedtest import Speedtest
from helpers.decorators import errors, admin_only
from helpers.filters import command

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@Client.on_message(filters.command(["stats",f"stats@{BOT_USERNAME}"]))
async def stats(client, message):
  if message.from_user.id in SUDO_USERS:  
    currentTime = get_readable_time(time.time() - botStartTime)
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    await message.reply_animation(animation='https://telegra.ph/file/fd2495f0465f5293bd052.mp4', caption=f"**≧◉◡◉≦ {BOT_NAME} is Up and Running successfully.**\n\n**⚙️ Bot Stats Of {BOT_NAME}⚙️**\n\n× Bot Uptime: `{currentTime}`\n× Total Disk Space: `{total}`\n× Used: `{used}({disk_usage}%)`\n× Free: `{free}`\n× CPU Usage: `{cpu_usage}%`\n× RAM Usage: `{ram_usage}%`",
                    parse_mode='Markdown', quote=True)
    
 #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@Client.on_message(filters.command(["ping",f"ping@{BOT_USERNAME}"]))
@admin_only
async def ping(_, message: Message):
   start = kek.now()
   m = await message.reply("**PONG!**")
   end = kek.now()
   pon = (end - start).microseconds / 1000
   await m.edit(f"**PONG!\nPing Time: `{pon}`")

 #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    
@Client.on_message(filters.command(["speedtest",f"speedtest@{BOT_USERNAME}"]))
async def speed(_, message: Message):
  if message.from_user.id in SUDO_USERS:
    imspd = await message.reply("`Running speedtest...`")
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    path = (result['share'])
    string_speed = f'''
× Upload: {human_readable_bytes(result["upload"] / 8)}/s
× Download: {human_readable_bytes(result["download"] / 8)}/s
× Ping: {result["ping"]} ms
× ISP: {result["client"]["isp"]}
'''
    await imspd.delete()
    await message.reply(string_speed)
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(command(["restrat", f"restart@{BOT_USERNAME}"]))
async def restart(client, message):
  if message.from_user.id in SUDO_USERS:
    await message.reply(f"`Restarting {BOT_NAME}..`")
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()
