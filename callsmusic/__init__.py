from pyrogram import Client
# from pyrogram import Client as Bot
import config

client = Client(config.SESSION_NAME, config.API_ID, config.API_HASH)
run = client.run
# client_bot = Bot("musicbot", config.API_ID, config.API_HASH, bot_token=config.BOT_TOKEN, plugins=dict(root="handlers"))
