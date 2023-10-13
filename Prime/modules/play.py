# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

import os
import asyncio
import re
from youtubesearchpython import SearchVideos
from pytgcalls import GroupCallFactory
from pyrogram import filters
from yt_dlp import YoutubeDL
from Prime import app, CMD_HELP
from config import PREFIX
from pytube import YouTube



CMD_HELP.update(
    {
        "play": f"""
『 **Play** 』
  `{PREFIX}play` [bales atau link] -> Memutar musik.
  `{PREFIX}vplay` [bales atau link] -> Memutar video.
  `{PREFIX}end` -> Menghentikan musik.
  `{PREFIX}vend` -> Menghentikan video.
"""
    }
)

MUSIK_LOGO = "https://telegra.ph/file/6213d2673486beca02967.png"

def video_link_getter(url: str, key=None):
    try:
        yt = YouTube(url)
        if key == "v":
            x = yt.streams.filter(file_extension="mp4", res="720p")[0].download()
        elif key == "a":
            x = yt.streams.filter(only_audio=True, type="audio")[0].download()
        return x
    except Exception as e:
        print(str(e))
        return 500
        
def yt_video_search(message: str):
    try:
        search = SearchVideos(str(message), offset=1, mode="dict", max_results=1)
        rt = search.result()
        result_s = rt["search_result"]
        url = result_s[0]["link"]
        return url
    except Exception as e:
        print(str(e))
        return 404
            

STREAM = {8}
VOICE_CALLS = {}
VIDEO_CALLS = {}

@app.on_message(filters.command("end", PREFIX) & filters.me)
async def leave_vc(client, message):
    CHAT_ID = message.chat.id
    oh = await app.get_chat(CHAT_ID)
    if not str(CHAT_ID).startswith("-100"): return
    voice_call = VOICE_CALLS.get(CHAT_ID)
    if voice_call:
        await voice_call.stop()
        await message.edit(f"**Musik telah di hentikan di**\n{oh.title}")

@app.on_message(filters.command("vend", PREFIX) & filters.me)
async def leave_vcd(client, message):
    CHAT_ID = message.chat.id
    oh = await app.get_chat(CHAT_ID)
    if not str(CHAT_ID).startswith("-100"): return
    video_call = VIDEO_CALLS.get(CHAT_ID)
    if video_call:
        await video_call.stop()
        await message.edit(f"**Video telah di hentikan di**\n{oh.title}")
        
@app.on_message(filters.command("play", PREFIX) & filters.me)
async def play_vc(client, message):
    CHAT_ID = message.chat.id
    ah = await app.get_chat(CHAT_ID)
    oh = await app.get_me()
    if not str(CHAT_ID).startswith("-100"): return
    msg = await message.edit("⏳ __Tolong Tunggu.__")
    media = message.reply_to_message
    if media:
        await msg.edit("📥 __Downloading...__")
        LOCAL_FILE = await app.download_media(media)
    else:
        try: INPUT_SOURCE = message.text.split(" ", 1)[1]
        except IndexError: return await msg.edit("🔎 __Tolong Berikan saya url youtube.__`")
        if ("youtube.com" in INPUT_SOURCE) or ("youtu.be" in INPUT_SOURCE):
            FINAL_URL = INPUT_SOURCE
            print(FINAL_URL)
        else:
            FINAL_URL = yt_video_search(INPUT_SOURCE)
            print(FINAL_URL)
            if FINAL_URL == 404:
                return await msg.edit("__Tidak menemukan Audio__ 🤷‍♂️")
        await msg.edit("📥 __Downloading...__")
        LOCAL_FILE = video_link_getter(FINAL_URL, key="a")
        if LOCAL_FILE == 500: return await msg.edit("__Download Error.__ 🤷‍♂️")
         
    try:
        voice_call = VOICE_CALLS.get(CHAT_ID)
        if voice_call is None:
            voice_call = GroupCallFactory(app, outgoing_audio_bitrate_kbit=512).get_group_call()
            VOICE_CALLS[CHAT_ID] = voice_call
        if voice_call.is_connected:
            await voice_call.stop()
            await asyncio.sleep(3)
        await voice_call.join(CHAT_ID)
        if not media:
            await app.send_photo(CHAT_ID, FINAL_URL, caption=f"**🚩 Streaming Musik di :**\n{ah.title}\n**⚡ Permintaan :** {oh.mention}\n✨ PRIME-USERBOT ✨")
        else:
            await app.send_photo(CHAT_ID, MUSIK_LOGO, caption=f"**🚩 Streaming Musik di :**\n{ah.title}\n**⚡ Permintaan :** {oh.mention}\n✨ PRIME-USERBOT ✨")
        await msg.delete()
        await voice_call.start_audio(LOCAL_FILE, repeat=False)
    except Exception as e:
        await message.edit(str(e))
        return await voice_call.stop()
    finally:
        await asyncio.sleep(20)
        os.remove(LOCAL_FILE)
        
        
@app.on_message(filters.command("vplay", PREFIX) & filters.me)        
async def stream_vc(client, message):
    CHAT_ID = message.chat.id
    ah = await app.get_chat(CHAT_ID)
    oh = await app.get_me()
    if not str(CHAT_ID).startswith("-100"): return
    msg = await message.edit("⏳ __Tolong Tunggu.__")
    media = message.reply_to_message
    if media:
        await msg.edit("📥 __Downloading...__")
        LOCAL_FILE = await app.download_media(media)
    else:
        try: INPUT_SOURCE = message.text.split(" ", 1)[1]
        except IndexError: return await msg.edit("🔎 __Tolong Berikan saya url youtube.__")
        if ("youtube.com" in INPUT_SOURCE) or ("youtu.be" in INPUT_SOURCE):
            FINAL_URL = INPUT_SOURCE
            print(FINAL_URL)
        else:
            FINAL_URL = yt_video_search(INPUT_SOURCE)
            print(FINAL_URL)
            if FINAL_URL == 404:
                return await msg.edit("__Tidak menemukan Video__ 🤷‍♂️")
        await msg.edit("📥 __Downloading...__")
        LOCAL_FILE = video_link_getter(FINAL_URL, key="v")
        if LOCAL_FILE == 500: return await msg.edit("__Download Error.__ 🤷‍♂️")
         
    try:
        video_call = VIDEO_CALLS.get(CHAT_ID)
        if video_call is None:
            video_call = GroupCallFactory(app, outgoing_audio_bitrate_kbit=512).get_group_call()
            VIDEO_CALLS[CHAT_ID] = video_call
        if video_call.is_connected:
            await video_call.stop()
            await asyncio.sleep(3)
        await video_call.join(CHAT_ID)
        if not media:
            await app.send_photo(CHAT_ID, FINAL_URL, caption=f"**🚩 Streaming Video di :**\n{ah.title}\n**⚡ Permintaan :** {oh.mention}\n✨ PRIME-USERBOT ✨")
        else:
            await app.send_photo(CHAT_ID, MUSIK_LOGO, caption=f"**🚩 Streaming Video di :**\n{ah.title}\n**⚡ Permintaan :** {oh.mention}\n✨ PRIME-USERBOT ✨")
        await msg.delete()
        await video_call.start_video(LOCAL_FILE, repeat=False)
    except Exception as e:
        await message.edit(str(e))
        return await video_call.stop()
    finally:
        await asyncio.sleep(20)
        os.remove(LOCAL_FILE)
