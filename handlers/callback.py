import asyncio
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from yt_dlp import YoutubeDL
from helpers.player import play_song

ydl_opts = {
    "format": "bestaudio/best",
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "%(id)s.%(ext)s",
}

ydl = YoutubeDL(ydl_opts)


@Client.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()


@Client.on_callback_query(filters.regex("choose_.*"))
async def chosse(client, query: CallbackQuery):
    m = query.message
    qvars = query.data.split("_", 2)
    url = qvars[2]
    user_id = int(qvars[1])
    r_user = await client.get_users(user_id)
    requested_by = "Anonymous"
    if r_user.first_name:
        requested_by = r_user.first_name
    link = f"https://youtube.com/watch?v={url}"
    song = ydl.extract_info(link, False)
    is_queue = await play_song(client, m, song, requested_by)
    if is_queue:
        await m.edit_text("*️⃣ Song queued")
    await asyncio.sleep(3)
    await m.delete()
