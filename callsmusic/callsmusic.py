from typing import Dict

from pytgcalls import GroupCallFactory
from pyrogram import Client as Bot
from . import queues
from . import client
import asyncio
from helpers.player import play_song
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

instances: Dict[int, GroupCallFactory] = {}
active_chats: Dict[int, Dict[str, bool]] = {}
waiting: Dict[int, bool] = {}
cover_message: Dict[int, int] = {}
client_bot: Bot = None
# current_raw: Dict[int, str] = {}


def init_instance(chat_id: int):
    if chat_id not in instances:
        instances[chat_id] = GroupCallFactory(client,outgoing_audio_bitrate_kbit=320).get_file_group_call()
        waiting[chat_id] = False

    instance = instances[chat_id]

    @instance.on_playout_ended
    async def ___(__, _):
        if not waiting[chat_id]:
            waiting[chat_id] = True
            queues.task_done(chat_id)
            try:
                await cover_message[chat_id].delete()
            except:
                logging.info('Cover already deleted')

            if queues.is_empty(chat_id):
                await stop(chat_id)
                m = await client_bot.send_message(chat_id, "Done")
                waiting[chat_id] = False
                await asyncio.sleep(3)
                await m.delete()
            else:
                song = queues.get(chat_id)
                input_filename = None
                m = await client_bot.send_message(chat_id, "🔄 Processing...")
                if "file" in song.keys():
                    input_filename = song["file"]
                await play_song(client_bot, m, song, song["requested_by"], file=input_filename, force=True)
                await m.delete()
                await asyncio.sleep(2)
                waiting[chat_id] = False
                
def remove(chat_id: int):
    if chat_id in instances:
        del instances[chat_id]

    if chat_id in active_chats:
        del active_chats[chat_id]
        queues.clear(chat_id)

def get_instance(chat_id: int) -> GroupCallFactory:
    init_instance(chat_id)
    return instances[chat_id]


async def start(chat_id: int):
    await get_instance(chat_id).start(chat_id)
    active_chats[chat_id] = {"playing": True, "muted": False}


async def stop(chat_id: int):
    await get_instance(chat_id).stop()

    if chat_id in active_chats:
        del active_chats[chat_id]


async def set_stream(chat_id: int, file: str):
    if chat_id not in active_chats:
        await start(chat_id)
    get_instance(chat_id).input_filename = file


def pause(chat_id: int) -> bool:
    if chat_id not in active_chats:
        return False
    elif not active_chats[chat_id]["playing"]:
        return False

    get_instance(chat_id).pause_playout()
    active_chats[chat_id]["playing"] = False
    return True


def resume(chat_id: int) -> bool:
    if chat_id not in active_chats:
        return False
    elif active_chats[chat_id]["playing"]:
        return False

    get_instance(chat_id).resume_playout()
    active_chats[chat_id]["playing"] = True
    return True


async def mute(chat_id: int) -> int:
    if chat_id not in active_chats:
        return 2
    elif active_chats[chat_id]["muted"]:
        return 1

    await get_instance(chat_id).set_is_mute(True)
    active_chats[chat_id]["muted"] = True
    return 0


async def unmute(chat_id: int) -> int:
    if chat_id not in active_chats:
        return 2
    elif not active_chats[chat_id]["muted"]:
        return 1

    await get_instance(chat_id).set_is_mute(False)
    active_chats[chat_id]["muted"] = False
    return 0
