from pyrogram import Client, filters
from pyrogram.types import Message, Voice
from youtube_search import YoutubeSearch 
from sunutils import group_call, quu, block_chat, FFMPEG_PRO, yt_download
import sunutils
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.types.input_stream import InputVideoStream, VideoParameters, InputAudioStream, AudioParameters
from pytgcalls import StreamType
import converter
from pyrogram.errors import exceptions
from helpers.filters import command, other_filters
from helpers.decorators import errors
from helpers.decorators import authorized_users_only
from helpers.decorators import authorized_users_only2
from helpers.gets import get_url
from config import BOT_USERNAME
import os
import signal

@group_call.on_stream_end()   
async def on_call_ended(client: PyTgCalls, update: Update):
  if update.chat.id in quu and len(quu[update.chat.id]) != 1:
    det = quu[update.chat_id][1]
    audio, video = det[1][0], det[1][1]
    await group_call.change_stream(
      update.chat_id,
      InputAudioStream(
        audio,
        AudioParameters(
          bitrate=48000,
          ),
        ),
      InputVideoStream(
        video,
        VideoParameters(
          width=640,
          height=360,
          frame_rate=20,
          ),
        ),
      stream_type=StreamType().local_stream,
    )
    quu[update.chat_id].pop(0)
  else:
    loop_stream = quu[update.chat_id][0]
    audio, video = loop_stream[1][0], loop_stream[1][1]
    await group_call.change_stream(
      update.chat.id,
      InputAudioStream(
        audio,
        AudioParameters(
          48000,
          ),
        ),
      InputVideoStream(
        video,
        VideoParameters(
          height=640,
          width=360,
          frame_rate=20,
          ),
        ),
      stream_type=StreamType().local_stream
      )
    #del quu[update.chat_id]

@Client.on_message(filters.command(['reset', f'reset@{BOT_USERNAME}']) & other_filters)
async def reset(_, message: Message):
  try:
    del quu[message.chat.id] 
  except Exception:
    pass
  try:
    await group_call.leave_group_call(message.chat.id)
  except Exception:
    pass
  await message.reply_text('Reset successful!')

@Client.on_message(filters.command(['skip', f'skip@{BOT_USERNAME}']) & other_filters)
async def skip(_, message: Message):
  if message.chat.id in quu and len(quu[message.chat.id]) != 1:
    det = quu[message.chat_id][1]
    audio, video = det[1][0], det[1][1]
    await group_call.change_stream(
      message.chat_id,
      InputAudioStream(
        audio,
        AudioParameters(
          bitrate=48000,
          ),
        ),
      InputVideoStream(
        video,
        VideoParameters(
          width=640,
          height=360,
          frame_rate=20,
          ),
        ),
      stream_type=StreamType().local_stream,
    )
    await message.reply_text(f'Skipped to {det[0]}')
    quu[message.chat_id].pop(0)
  else:
    try:
      await group_call.leave_group_call(message.chat.id)
      del quu[message.chat.id] 
    except Exception:
      pass 
    await message.reply_text('Nothing to skip!')

@Client.on_message(filters.command(["stream", f"stream@{BOT_USERNAME}"]) & other_filters)
async def stream(client: Client, message: Message):
  video = (message.reply_to_message.video or message.reply_to_message.document) if message.reply_to_message else None
  url = get_url(message)
  if video and (video.file_name.endswith('.mkv') or video.file_name.endswith('.mp4')):
    m = await message.reply_text('Downloading....will take time depending on video size...')
    file_name = f'{video.file_unique_id}.{video.file_name.split(".", 1)[-1]}'
    dl = await message.reply_to_message.download(file_name)
    try:
      subska = message.text.split(' ', 1)[1]
      if subska.startswith('atr'):
        try:
          configg = subska.split(':')
          subconfig = configg[1]
        except IndexError:
          subconfig = 0
        await m.edit('Burning subs!.., who knows how much time will it take..')
        dl = await converter.burn_subs(dl, sub=subconfig)
    except IndexError:
      pass
    video_name = video.file_name.split('.', 1)[0]
    audio, video = await converter.convert(dl)
  elif url:
    m = await message.reply('Downloading..')
    yt, video_name = await yt_download(url)
    audio, video = await converter.convert(yt)
  await m.edit("Joining...")
  if message.chat.id in quu:
    quu[message.chat.id].append([
      video_name,
      (audio, video),
      ])
    await message.reply(f'Added to queue in postion {len(quu[message.chat.id])}')
  else:
    await group_call.join_group_call(
      message.chat.id,
      InputAudioStream(
        audio,
        AudioParameters(
          bitrate=48000,
          ),
        ),
      InputVideoStream(
        video,
        VideoParameters(
          width=640,
          height=360,
          frame_rate=20,
          ),
        ),
      stream_type=StreamType().local_stream,
    )
    quu[message.chat.id] = []
    quu[message.chat.id].append([video_name, (audio, video)])
    await message.reply_text(f'Streaming ...')

@Client.on_message(filters.command(['live', f'live@{BOT_USERNAME}']) & other_filters)
async def llivestream(_, message: Message):
  try:
    url = message.text
    video = f'streamvid{message.chat.id}.raw'
    audio = f'streamaud{message.chat.id}.raw'
    proc = converter.live_converter(url, video, audio)
    FFMPEG_PRO[message.chat.id] = proc
    await group_call.join_group_call(
      message.chat.id,
      InputAudioStream(
        audio,
        AudioParameters(
          48000,
          ),
        ),
      InputVideoStream(
        video,
        VideoParameters(
          height = 1280,
          width = 720,
          frame_rate = 25,
          ),
        ),
      )
  except IndexError:
    await message.reply_text('Url piliz!')

@Client.on_message(filters.command(['stop', f'stop{BOT_USERNAME}']) & other_filters)  
async def stop(_, message: Message):
  if message.chat.id in FFMPEG_PRO:
    proc = FFMPEG_PRO[message.chat.id]
    proc.send_signal(signal.SIGQUIT)
    FFMPEG_PRO.remove(message.chat.id)
    await group_call.leave_group_call(message.chat.id)
  if message.chat.id in quu:
    await group_call.leave_group_call(message.chat.id)
    await message.reply('left!')
    del quu[message.chat.id]
  else:
    await message.reply_text('Not streaming...')
  