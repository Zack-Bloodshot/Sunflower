from helpers.filters import command, other_filters2, other_filters
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from config import BOT_USERNAME 
from youtubesearchpython import VideosSearch
import converter
import config 

@Client.on_message(command("start") & other_filters)
async def start(_, message: Message):
    await message.reply_text('Im sunflower ~')

@Client.on_inline_query()
async def inline(client: Client, query: InlineQuery):
    answers = []
    search_query = query.query.lower().strip().rstrip()

    if search_query == "":
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text="Type a YouTube video name...",
            switch_pm_parameter="help",
            cache_time=0
        )
    else:
        search = VideosSearch(search_query, limit=50)
        
        for result in search.result()["result"]:
            idt = result['id']
            tit = result['title']
            answers.append(
                InlineQueryResultArticle(
                    title=result["title"],
                    description="{}, {} views.".format(
                        result["duration"],
                        result["viewCount"]["short"]
                    ),
                    input_message_content=InputTextMessageContent(
                        f"/stream@{BOT_USERNAME} https://youtu.be/{idt}\n\n{tit}", disable_web_page_preview = True
                    ),
                    thumb_url=result["thumbnails"][0]["url"]
                )
            )

        try:
            await query.answer(
                results=answers,
                cache_time=0
            )
        except errors.QueryIdInvalid:
            await query.answer(
                results=answers,
                cache_time=0,
                switch_pm_text="Error: Search timed out",
                switch_pm_parameter="",
            )
            
@Client.on_message(filters.command(['sub', f'sub@{BOT_USERNAME}']), other_filters)
async def subsend(_, message: Message):
  video = (message.reply_to_message.video or message.reply_to_message.document) if message.reply_to_message else None
  if video:
    dl = await video.dowmload()
    m = await message.reply_message('Burning subs...')
    ff = await converter.burn_subs(dl)
    await m.edit('Uploading....')
    await message.reply_document(ff)
    await m.delete()
    
@Client.on_message(filters.command(['logs', f'logs@{BOT_USERNAME}']))
async def logsend(_, message: Message):
  try:
    await message.reply_document(document='bot.log')
  except BaseException:
    await message.reply('Some error happend..F')