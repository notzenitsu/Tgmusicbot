import asyncio
import converter
import logging
from os import path
from pyrogram import Client
from typing import Union
from pyrogram.types import Message, Voice, Audio
from yt_dlp import YoutubeDL
from config import DURATION_LIMIT, BOT_USERNAME
from helpers.errors import DurationLimitError
from helpers.filters import command, other_filters
from helpers.decorators import errors, authorized_users_only
from helpers.player import ytplay, play_song

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

ydl_opts = {
    "format": "bestaudio/best",
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "%(id)s.%(ext)s",
}

ydl = YoutubeDL(ydl_opts)

def get_file_name(audio: Union[Audio, Voice]):
    return f'{audio.file_unique_id}.{audio.file_name.split(".")[-1] if not isinstance(audio, Voice) else "ogg"}'

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(command(["play", f"play@{BOT_USERNAME}"]) & other_filters)
@errors
async def play(client, message: Message):
    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    file = None
    requested_by = "Anonymous"
    if message.from_user.first_name:
        requested_by = message.from_user.first_name
    user_id = message.from_user.id

    res = await message.reply_text("🔄 Processing...")

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"Videos longer than {DURATION_LIMIT} minute(s) aren't allowed, the provided video is {audio.duration / 60} minute(s)"
            )
        title = audio.title
        song = {}
        song['title'] = title
        song['duration'] = round(audio.duration / 60)
        song['view_count'] = 0
        song['thumbnail'] = "https://telegra.ph/file/f6086f8909fbfeb0844f2.png"
        file_name = get_file_name(audio)
        file = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
        if await play_song(client, res, song, requested_by, file):
            await res.edit_text("*️⃣ Song queued")
    else:
        messages = [message]
        text = ""
        offset = None
        length = None

        if message.reply_to_message:
            messages.append(message.reply_to_message)

        isnoturl = True
        for _message in messages:
            if offset:
                break

            if _message.entities:
                for entity in _message.entities:
                    if entity.type == "url":
                        text = _message.text or _message.caption
                        offset, length = entity.offset, entity.length
                        isnoturl = False
                        break

        if not isnoturl and offset in (None,):
            await res.edit_text("❗️ You did not give me anything to play.")
            return
        if isnoturl:
            query = message.text.split(None, 1)[1:]
            await ytplay(client, message.chat.id, user_id, query)
            file = None
        else:
            url = text[offset:offset + length]
            info = ydl.extract_info(url, False)
            is_queue = False
            if '_type' in info.keys() and info['_type'] == 'playlist':
                q_songs = 0
                for song in info['entries']:
                    is_queue = await play_song(client, res, song, requested_by)
                    if is_queue:
                        q_songs += 1
                if q_songs > 0:
                    await res.edit_text(f"*️⃣ {q_songs} songs queued")
            else:
                await play_song(client, res, info, requested_by)
    await asyncio.sleep(3)
    await res.delete()
    
 #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
