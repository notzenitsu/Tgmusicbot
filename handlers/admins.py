from pyrogram import Client
from pyrogram.types import Message
from helpers.filters import command
from helpers.decorators import authorized_users_only
from helpers.redis import Redis
from helpers import errors

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@Client.on_message(command(["onadmin", "offadmin"]))
@authorized_users_only
async def adminMode(client, message: Message):
    cmd = message.command[0].strip('/')
    if cmd == 'onadmin':
        await Redis.set("adminOnly", True)
        await message.reply("Enabled Admin-Only Mode.")
    else:
        await Redis.set("adminOnly", False)
        await message.reply("Disabled Admin-Only Mode.")
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
