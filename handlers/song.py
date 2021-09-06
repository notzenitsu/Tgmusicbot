import os
import yt_dlp
import requests
from pyrogram import Client
from pyrogram.types import Message, Voice, InlineKeyboardMarkup, InlineKeyboardButton
from youtube_search import YoutubeSearch
from helpers.filters import command, other_filters
from helpers.decorators import errors, admin_only
from config import BOT_USERNAME, BOT_NAME

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(command(["song", f"song@{BOT_USERNAME}"]) & other_filters)
@errors
@admin_only
async def song(client, message: Message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    okvai = query.capitalize()
    print(query.capitalize())
    m = await message.reply(f"🔍 Searching for {okvai}")
    ydl_opts = {
      "format": "bestaudio",
      "addmetadata": True,
      "geo-bypass": True,
      "outtmpl": "%(id)s.mp3",
    }
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            await m.edit(f"Found nothing. Try changing the spelling a little.\n\n{e}")
            return
    except Exception as e:
        await m.edit(
           f"Ahh, Found Nothing. Sorry.\nTry another keywork or maybe spell it properly."
        )
        print(str(e))
        return
    await m.edit(f"Downloading.. **{query}**" )
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'[{title[:35]}]({link}) | [{BOT_NAME}](https://t.me/{BOT_USERNAME})'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        await  message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name)
        await m.delete()
    except Exception as e:
        await m.edit(f"❗️ Error!! \n\n{e}")
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
        
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
