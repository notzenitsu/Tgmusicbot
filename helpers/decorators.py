import logging
from typing import Callable
from pyrogram import Client
from pyrogram.types import Message
from helpers.admins import get_administrators
from helpers.redis import Redis
from helpers.functions import isAdmin
from config import SUDO_USERS
from pyrogram.types import CallbackQuery

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def errors(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        try:
            return await func(client, message)
        except Exception as e:
            await message.reply(f"{type(e).__name__}: {e}")

    return decorator
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def authorized_users_only(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        if message.from_user.id in SUDO_USERS:
            return await func(client, message)

        administrators = await get_administrators(message.chat)

        for administrator in administrators:
            if administrator == message.from_user.id:
                return await func(client, message)

    return decorator
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def admin_only(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        if await Redis.get('adminOnly'):
            if await isAdmin(client, message.chat.id, message.from_user.id):
                return await func(client, message)
        else:
            return await func(client, message) 
        
    return decorator
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
