import random 
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from helpers.filters import command
from config import BOT_USERNAME, BOT_NAME, ASSISTANT_USERNAME, SUPPORT_GROUP



#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(filters.private & filters.incoming & filters.command(['start']))
async def start(_, message: Message):
     await message.reply_animation(animation='https://telegra.ph/file/c0857672b427bec8542f6.mp4', caption=f"I am {BOT_NAME}, A Music Player bot that lets you play music in your groups via voice chats. Add me and my assistant @{ASSISTANT_USERNAME} in your group to play music", parse_mode="markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ Add me to your Group ➕ ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
                [
                    InlineKeyboardButton(
                        "🙎‍ Assistant", url=f"https://t.me/{ASSISTANT_USERNAME}"), 
                    InlineKeyboardButton(
                        "💬 Support", url=f"https://t.me/{SUPPORT_GROUP}")
                ],[
                    InlineKeyboardButton(
                        "🔭 Original Repo", url=f"https://github.com/CallsMusic/CallsMusic")
                ]
            ]
        ),
        reply_to_message_id=message.message_id
        )

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(filters.command("start") & ~filters.private & ~filters.channel)
async def gstart(_, message: Message):
    await message.reply_text(
        f"""**{BOT_NAME} is online**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "How to use me?", url=f"https://t.me/{BOT_USERNAME}?start=help"
                    )
                ]
            ]
            
            
        ),
    )

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
