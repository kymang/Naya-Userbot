# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
# abdul
#
# All rights reserved.

import os
import asyncio
from pyrogram import filters
from pyrogram.errors import RPCError
from Prime import CMD_HELP, app
from config import PREFIX
from Prime.helpers.pyrohelper import get_arg

CMD_HELP.update(
    {
        "nyolong": f"""
『 **Nyolong** 』
  `{PREFIX}nyolong` -> Mengcopy apapun dari channel yang di protect.
  `{PREFIX}curi` -> Mengcopy apapun dari bot yang di protect.
  `{PREFIX}effect` -> Untuk mengubah vn jadi suara `bengek` | `robot` | `jedug` | `fast` | `echo`
"""
    }
)


@app.on_message(filters.command("nyolong", PREFIX) & filters.me)
async def nyolongnih(client, message):
    link = get_arg(message)
    if link.startswith("https"):
        msg_id = int(link.split("/")[-1])
        await message.edit("Nyolong konten dulu cuy")
        if 't.me/c/' in link:
            try:
                chat = int('-100' + str(link.split("/")[-2]))
                dia = await app.get_messages(chat, msg_id)
            except RPCError:
                await message.edit("Sepertinya ada yang salah")
        else:
            try:
                chat = str(link.split("/")[-2])
                dia = await app.get_messages(chat, msg_id)
            except RPCError:
                await message.edit("Sepertinya ada yang salah")
        anjing = dia.caption or None
        if dia.text:
            await dia.copy(message.chat.id)
            await message.delete()
            
        if dia.sticker:
            await dia.copy(message.chat.id)
            await message.delete()
                    
        if dia.photo:
            anu = await app.download_media(dia)
            await app.send_photo(message.chat.id, anu, anjing)
            await message.delete()
            os.remove(anu)
        
        if dia.video:
            anu = await app.download_media(dia)
            await app.send_video(message.chat.id, anu, anjing)
            await message.delete()
            os.remove(anu)
        
        if dia.audio:
            anu = await app.download_media(dia)
            await app.send_audio(message.chat.id, anu, anjing)
            await message.delete()
            os.remove(anu)
        
        if dia.voice:
            anu = await app.download_media(dia)
            await app.send_voice(message.chat.id, anu, anjing)
            await message.delete()
            os.remove(anu)
        
        if dia.document:
            anu = await app.download_media(dia)
            await app.send_document(message.chat.id, anu, anjing)
            await message.delete()
            os.remove(anu)
            
        if dia.animation:
            anu = await app.download_media(dia)
            await app.send_animation(message.chat.id, anu, anjing)
            await message.delete()
            os.remove(anu)
            
        else:
            await message.edit("Sepertinya ada yang salah")
    else:
        await message.edit("Silahkan kombinasikan command dan link")
    
    
@app.on_message(filters.command("curi", PREFIX) & filters.me)
async def pencuri(client, message):
    dia = message.reply_to_message
    if not dia:
        await message.edit("Silahkan balas ke media di bot")
    anjing = dia.caption or None
    await message.edit("Siap mencuri konten...")
    if dia.text:
        await dia.copy(message.chat.id)
        await message.delete()
    if dia.photo:
        anu = await app.download_media(dia)
        await app.send_photo(message.chat.id, anu, anjing)
        await message.delete()
        os.remove(anu)
        
    if dia.video:
        anu = await app.download_media(dia)
        await app.send_video(message.chat.id, anu, anjing)
        await message.delete()
        os.remove(anu)
        
    if dia.audio:
        anu = await app.download_media(dia)
        await app.send_audio(message.chat.id, anu, anjing)
        await message.delete()
        os.remove(anu)
        
    if dia.voice:
        anu = await app.download_media(dia)
        await app.send_voice(message.chat.id, anu, anjing)
        await message.delete()
        os.remove(anu)
        
    if dia.document:
        anu = await app.download_media(dia)
        await app.send_document(message.chat.id, anu, anjing)
        await message.delete()
        os.remove(anu)
    else:
        await message.edit("Sepertinya ada yang salah")
    
@app.on_message(filters.command("effect", PREFIX) & filters.me)
async def effectku(client, message):
    helo = get_arg(message)
    rep = message.reply_to_message
    if rep and helo:
        tau = ["bengek", "robot", "jedug", "fast", "echo"]
        if helo in tau:
            await message.edit(f"Merubah suara menjadi {helo}")
            indir = await app.download_media(rep)
            KOMUT = {
                 "bengek": '-filter_complex "rubberband=pitch=1.5"',
                 "robot": "-filter_complex \"afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=512:overlap=0.75\"",
                 "jedug": '-filter_complex "acrusher=level_in=8:level_out=18:bits=8:mode=log:aa=1"',
                 "fast": "-filter_complex \"afftfilt=real='hypot(re,im)*cos((random(0)*2-1)*2*3.14)':imag='hypot(re,im)*sin((random(1)*2-1)*2*3.14)':win_size=128:overlap=0.8\"",
                 "echo": '-filter_complex "aecho=0.8:0.9:500|1000:0.2|0.1"',
                }
            ses = await asyncio.create_subprocess_shell(
                        f"ffmpeg -i '{indir}' {KOMUT[helo]} kontol.mp3"
                    )
            await ses.communicate()
            await message.delete()
            await rep.reply_voice("kontol.mp3", caption=f"Effect {helo}")
            os.remove("kontol.mp3")
        else:
            await message.edit(f"Silahkan isi sesuai {tau}")
    else:
        await message.edit(f"Silahkan balas ke audio atau mp3, contoh : `{PREFIX}effect bengek` sambil balas ke audio atau mp3")