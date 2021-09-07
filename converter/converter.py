import os
import asyncio
import ffmpeg
import json

async def get_video_info(file_path):
    proc = await asyncio.create_subprocess_shell(f'ffprobe -hide_banner -print_format json -show_format -show_streams {file_path}', stdout=asyncio.subprocess.PIPE)
    stdout, _ = await proc.communicate()
    return json.loads(stdout)

async def burn_subs(file_path: str, sub=0):
  sub_out = str(file_path).split('.', 1)[0] + 'sub.ass'
  video_ext = str(file_path).split('.', 1)[1]
  video_out = str(file_path).split('.', 1)[0] + f'_burnsubs.{video_ext}'
  proc = await asyncio.create_subprocess_shell(
    f"ffmpeg -i {file_path} -map 0:s:{sub} {sub_out}",
    asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE
    )
  await proc.communicate()
  proc = await asyncio.create_subprocess_shell(
    f"ffmpeg -i {file_path} -vf subtitles={sub_out} -c:a copy -y {video_out}",
    asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE
    )
  print('Burning subs...')
  await proc.communicate()
  os.remove(file_path)
  return video_out
  

async def convert(file_path: str, dell=True) -> str:
    out_audio = str(file_path).split('.', 1)[0] + 'audio.raw'
    out_video = str(file_path).split('.', 1)[0] + 'video.raw'
    if os.path.isfile(out_audio) & os.path.isfile(out_video):
        return out_audio, out_video
  
    proc = await asyncio.create_subprocess_shell(
        f"ffmpeg -i {file_path} -f s16le -ac 1 -ar 48000 {out_audio} -f rawvideo -r 30 -pix_fmt yuv420p -vf scale=640:-1 {out_video}",
        asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    print('Vid and Audio converison..')
    await proc.communicate()
    if dell==True:
      os.remove(file_path)
    return out_audio, out_video

def live_converter(source, vid, audio):
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", source, "-f", "s16le", "-ac", "1", "-ar", "48000", audio, "-f", "rawvideo", '-r', '25', '-pix_fmt', 'yuv420p', '-vf', 'scale=640:-1', vid]
    return subprocess.Popen(
        cmd,
        stdin=None,
        stdout=None,
        stderr=None,
        cwd=None,
    )