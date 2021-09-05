from pyrogram import Client
from pyrogram import filters
from pyrogram.raw import functions
from pyrogram.utils import MAX_CHANNEL_ID
from pytgcalls import PyTgCalls
import config
import asyncio

client = Client(config.SESSION_NAME, config.API_ID, config.API_HASH)
group_call = PyTgCalls(client)
quu = {} 
block_chat = []
GROUP_CALL = {}
FFMPEG_PRO = {}
          