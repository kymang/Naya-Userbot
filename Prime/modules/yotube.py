# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

import asyncio
import os
import time
import requests
import wget
from yt_dlp import YoutubeDL
from youtubesearchpython import SearchVideos
from pyrogram import filters

from Prime import CMD_HELP, app
from config import PREFIX

CMD_HELP.update(
    {
        "youtube": f"""
『 **YouTube** 』
  `{PREFIX}video` [link atau tulisan] -> Download video dari yt.
  `{PREFIX}song` [link atau tulisan] -> Download song dari yt.
"""
    }
)

@app.on_message(filters.command("video", PREFIX) & filters.me)
async def yt_vid(client, message):
    input_st = message.text
    input_str= input_st.split(" ", 1)[1]
    pablo = await message.edit_text("`Processing...`")
    if not input_str:
        await message.edit_text(
            "Tolong berikan input yang valid"
        )
        return
    await message.edit_text(f"`Searching {input_str} From Youtube. Please Wait.`")
    search = SearchVideos(str(input_str), offset=1, mode="dict", max_results=1)
    rt = search.result()
    result_s = rt["search_result"]
    url = result_s[0]["link"]
    vid_title = result_s[0]["title"]
    yt_id = result_s[0]["id"]
    uploade_r = result_s[0]["channel"]
    thumb_url = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    downloaded_thumb = wget.download(thumb_url)
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        await message.edit_text(f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    file_path= f"{ytdl_data['id']}.mp4"
    capy = f"**Video Name ➠** `{vid_title}` \n**Requested For ➠** `{input_str}` \n**Channel ➠** `{uploade_r}` \n**Link ➠** `{url}`"
    await app.send_video(
        message.chat.id,
        video=open(file_path, "rb"),
        duration=int(ytdl_data["duration"]),
        file_name=str(ytdl_data["title"]),
        thumb=downloaded_thumb,
        caption=capy,
        supports_streaming=True,
    )
    await message.delete()
    for files in (downloaded_thumb, file_path):
        if files and os.path.exists(files):
            os.remove(files)


@app.on_message(filters.command("song", PREFIX) & filters.me)
async def ytmusic(client, message):
    oh = message.text
    urlissed = oh.split(" ", 1)[1]
    if not urlissed:
        await message.edit("Invalid Command Syntax, Please Check Help Menu To Know More!",
        )
        return
    pablo = await message.edit(f"`Getting {urlissed} From Youtube Servers. Please Wait.`"
    )
    search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    mo = mio[0]["link"]
    song_title = mio[0]["title"]
    uploade_rs = mio[0]["channel"]
    opts = {
            'format':'bestaudio',
            'keepvideo':True,
            'prefer_ffmpeg':False,
            'geo_bypass':True,
            'outtmpl':'%(title)s.%(ext)s.mp3',
            'quite':True
        }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(mo, download=True)
            fname = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        await pablo.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    cap = f"**Song Name ➠** [{song_title}]({mo})\n**Channel ➠** `{uploade_rs}` \n**Link ➠** `{mo}`"
    await app.send_audio(
                message.chat.id,
                fname,
                caption=cap,
                performer=uploade_rs
                )
                
    await message.delete()
    await pablo.delete()
    os.remove(fname)
