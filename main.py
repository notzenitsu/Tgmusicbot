from pyrogram import Client as Bot
from callsmusic import run
from config import API_ID, API_HASH, BOT_TOKEN
from callsmusic import callsmusic as cm
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    workers=15,
    plugins=dict(root="handlers")
)
cm.client_bot = bot
bot.start()
run() 
