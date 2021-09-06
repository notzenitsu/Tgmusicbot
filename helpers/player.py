import converter
import youtube
from callsmusic import callsmusic, queues
from config import DURATION_LIMIT
from helpers.functions import convert_seconds, generate_cover
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import os
import logging
from youtubesearchpython import VideosSearch
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# search on youtube to play the song
async def ytplay(client, chat_id, requested_by, query):
    m = await client.send_message(chat_id, f"**Searching for {query} on YouTube.**", disable_web_page_preview=True)
    try:
        videosSearch = VideosSearch(query[0], limit=6)
        results = videosSearch.result()['result']
        # results = await arq.youtube(query[0], 6)
        text = "**Results:**\n\n"
        songbt = []
        for num in range(0, len(results) - 1):
            title = results[num]['title']
            duration = results[num]['duration']
            views = results[num]['viewCount']['short']
            url = f"{results[num]['id']}"
            text += f"  **{num + 1}.** **{title}** {duration} views: {views}\n\n"
            songbt.append(InlineKeyboardButton(f"{num + 1}", f'choose_{requested_by}_{url}'))
        await m.edit(text, reply_markup=InlineKeyboardMarkup([songbt]))
    except Exception as e:
        await m.edit("__**Found No Song Matching Your Query.**__")
        print(str(e))
        return


# play a file or add it to the queue
async def play_song(client, message, song, requested_by, file=None, force=False):
    duration = round(song["duration"] / 60)
    sduration_converted = convert_seconds(int(song['duration']))
    # song too long
    if DURATION_LIMIT < round(song["duration"] / 60):
        logging.info(f"Videos longer than {DURATION_LIMIT} minute(s) aren't allowed, the provided video is {duration} minute(s)")
        return False
    # check if a song is already playing
    if not force and message.chat.id in callsmusic.active_chats:
        # if has a file path it's an audio file and we don't need to convert it
        if file:
            logging.info(f"Queue: {file}")
            await queues.put(message.chat.id, file=file, title=song['title'], requested_by=requested_by, views=song['view_count'], thumbnail=song['thumbnail'], duration=song['duration'], id=song['id'], ext=song['ext'], duration_converted=sduration_converted)
        else:
            logging.info(f"Queue: {song['webpage_url']}")
            await queues.put(message.chat.id, webpage_url=song['webpage_url'], title=song['title'], requested_by=requested_by, view_count=song['view_count'], thumbnail=song['thumbnail'], duration=song['duration'], id=song['id'], ext=song['ext'], sduration_converted=sduration_converted)
        return True
    else:
        if file:
            logging.info(f"Playing: {file}")
        else:
            logging.info(f"Playing: {song['webpage_url']}")
            yt_path = youtube.download(song)
            file = await converter.convert(yt_path)
        img_path = await generate_cover(message.chat.id, requested_by, song['title'], song['view_count'], sduration_converted, song['thumbnail'])
        callsmusic.cover_message[message.chat.id] = await client.send_photo(chat_id=message.chat.id, caption=f"**Now Playing [{song['title']}]**", photo=img_path)
        os.remove(img_path)
        await callsmusic.set_stream(message.chat.id, file)
        return False
