from helpers.filters import command, other_filters2
from pyrogram import Client
from pyrogram.types import Message

@Client.on_message(command("start") & other_filters2)
async def start(_, message: Message):
    await message.reply_text('Im sunflower ~')