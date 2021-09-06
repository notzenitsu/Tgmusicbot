from asyncio import QueueEmpty
from pyrogram import Client
from pyrogram.types import Message
from callsmusic import callsmusic, queues
import asyncio
from helpers.filters import command
from helpers.decorators import errors, authorized_users_only, admin_only
from helpers.player import play_song
from config import  BOT_USERNAME

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(command(["pause", f"pause@{BOT_USERNAME}"]))
@errors
@admin_only
async def pause(_, message: Message):
    if callsmusic.pause(message.chat.id):
        await message.reply_text("⏸ Paused")
    else:
        await message.reply_text("❗️ Nothing is playing")
        
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@Client.on_message(command(["resume", f"resume@{BOT_USERNAME}"]))
@errors
@admin_only
async def resume(_, message: Message):
    if callsmusic.resume(message.chat.id):
        await message.reply_text("🎧 Resumed")
    else:
        await message.reply_text("❗️ Nothing is paused")
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(command(["stop", f"stop@{BOT_USERNAME}"]))
@errors
@admin_only
async def stop(_, message: Message):
    if message.chat.id not in callsmusic.active_chats:
        await message.reply_text("❗️ Nothing is playing")
    else:
        try:
            queues.clear(message.chat.id)
        except QueueEmpty:
            pass

        await callsmusic.stop(message.chat.id)
        await message.reply_text("✅ Cleared the queue and left the call")

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(command(["skip", f"skip@{BOT_USERNAME}"]))
@errors
@admin_only
async def skip(client, message: Message):
    if message.chat.id not in callsmusic.active_chats:
        await message.reply_text("❗️ Nothing is playing")
    else:
        queues.task_done(message.chat.id)
        chat_id = message.chat.id
        try:
            await callsmusic.cover_message[chat_id].delete()
        except:
            print('deleted')

        if queues.is_empty(message.chat.id):
            await callsmusic.stop(message.chat.id)
            m = await client.send_message(message.chat.id, "Done")
            await asyncio.sleep(3)
            await m.delete()
        else:
            song = queues.get(message.chat.id)
            input_filename = None
            m = await client.send_message(chat_id, "🔄 Processing...")
            if "file" in song.keys():
                input_filename = song["file"]
            await play_song(client, m, song, song["requested_by"], file=input_filename, force=True)
            await m.delete()

        sk = await message.reply_text("Skipped.")
        await asyncio.sleep(3)
        await sk.delete()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(command(["mute", f"mute@{BOT_USERNAME}"]))
@errors
@admin_only
async def mute(_, message: Message):
    result = callsmusic.mute(message.chat.id)

    if result == 0:
        await message.reply_text("🔇 Muted")
    elif result == 1:
        await message.reply_text("🔇 Already muted")
    elif result == 2:
        await message.reply_text("❗️ Not in voice chat")

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(command(["unmute", f"unmute@{BOT_USERNAME}"]))
@errors
@admin_only
async def unmute(_, message: Message):
    result = callsmusic.unmute(message.chat.id)

    if result == 0:
        await message.reply_text("🔈 Unmuted")
    elif result == 1:
        await message.reply_text("🔈 Already unmuted")
    elif result == 2:
        await message.reply_text("❗️ Not in voice chat")

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(command(["player", f"player@{BOT_USERNAME}"]))
async def listq(_, message: Message):
    if message.chat.id not in callsmusic.active_chats:
        await message.reply_text("❕ Nothing is streaming.")
    else:
        await message.reply_text("**Queue:-**\n\n" + queues.qlist(message.chat.id))
       
 #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
