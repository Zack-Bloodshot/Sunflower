from pyrogram import Client, filters
from pyrogram.types import Message, Voice
from youtube_search import YoutubeSearch 
from callsmusic import group_call, quu, block_chat, FFMPEG_PRO
from pytgcalls.types.input_stream import InputVideoStream
from pytgcalls import StreamType
import callsmusic
import converter
from pyrogram.errors import PeerIdInvalid, ChannelInvalid
from pyrogram.errors import exceptions
from downloaders import youtube
from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
from config import BOT_NAME as bn, DURATION_LIMIT
from helpers.filters import command, other_filters
from helpers.decorators import errors
from helpers.decorators import authorized_users_only
from helpers.decorators import authorized_users_only2
from config import API_ID, API_HASH, BOT_TOKEN, PLAY_PIC, BOT_USERNAME, OWNER_ID, UBOT_ID
import asyncio
import os
import ffmpeg

@Client.on_message(filters.command(["stream", f"stream@{BOT_USERNAME}"]) & other_filters)
async def stream(client: Client, message: Message):
  if message.chat.id in block_chat:
    m = await message.reply_text('Please stop present stream to start new....')
    asyncio.sleep(3)
    return await m.delete()
  video = (message.reply_to_message.video or message.reply_to_message.document) if message.reply_to_message else None
  if not video:
    return await message.reply_text('Reply to a file or a video....')
  if not (video.file_name.endswith('.mkv') or video.file_name.endswith('.mp4')):
    return await message.reply_text('Not a valid format...')
  m = await message.reply_text('Downloading....will take time depending on video size...')
  file_name = f'{video.file_unique_id}.{video.file_name.split(".", 1)[-1]}'
  dl = await message.reply_to_message.download(file_name)
  await group_call.join_group_call(
    message.chat.id,
    InputVideoStream(dl),
    48000,
    pytgcalls.cache_peer,
    StreamType().local_stream,
  )
  await message.reply_text(f'Streaming {video.file_name}...')
  block_chat.append(message.chat.id)
  
