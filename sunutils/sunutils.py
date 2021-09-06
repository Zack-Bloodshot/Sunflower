from pyrogram import Client
from pyrogram import filters
from pyrogram.raw import functions
from pyrogram.utils import MAX_CHANNEL_ID
from pytgcalls import PyTgCalls
import config
import asyncio
from youtube_dl import YoutubeDL

client = Client(config.SESSION_NAME, config.API_ID, config.API_HASH)
group_call = PyTgCalls(client)
quu = {} 
block_chat = []
GROUP_CALL = {}
FFMPEG_PRO = {}

async def yt_download(ytlink):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': '%(id)s-%(extractor)s.%(ext)s',
        'writethumbnail': False
    }
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(ytlink, download=False)
        ydl.process_info(info_dict)
        file = ydl.prepare_filename(info_dict)
        tit = info_dict.get('title')
        return file, tit