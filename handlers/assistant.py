from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
import asyncio
from helpers.decorators import authorized_users_only, errors
from callsmusic.callsmusic import client as USER
from config import BOT_USERNAME, BOT_NAME, ASSISTANT_USERNAME, SUPPORT_GROUP, SUDO_USERS


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(filters.command(["assistantjoin",f"assistantjoin@{BOT_USERNAME}"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Add me as admin of yor group first</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = f"{BOT_NAME}"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, f"{BOT_NAME} Assistant joined here for playing music in voice chats")
    except UserAlreadyParticipant:
        await message.reply_text(
            f"{BOT_NAME} Assistant already in chat",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Flood Wait Error 🛑\n@{ASSISTANT_USERNAME} couldn't join your group due to heavy join requests for userbot! Make sure user is not banned in group or it is not in removed user list.\nor manually add @{ASSISTANT_USERNAME} to your Group and try again</b>",
        )
        return
    await message.reply_text(
        f"{BOT_NAME} Assistant joined the chat",
    )

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@USER.on_message(filters.group & filters.command(["assistantleave", f"assistantleave@{BOT_USERNAME}"]))
@authorized_users_only
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            f"{BOT_NAME} Assistant couldn't leave the chat.kick the assistant manually",
        )
        return
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(filters.command(["assistantleaveall"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left=0
        failed=0
        lol = await message.reply("Assistant Leaving all chats")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left+1
                await lol.edit(f"Assistant leaving... Left: {left} chats. Failed: {failed} chats.")
            except:
                failed=failed+1
                await lol.edit(f"Assistant leaving... Left: {left} chats. Failed: {failed} chats.")
            await asyncio.sleep(0.7)
        await client.send_message(message.chat.id, f"Left {left} chats. Failed {failed} chats.")
    
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
