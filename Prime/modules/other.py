# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

import asyncio
import random
from asyncio import sleep
import requests
from pyrogram import filters, enums
from pyrogram.types import *
from pyrogram.errors import YouBlockedUser
from pyrogram.errors import PeerIdInvalid
from Prime.helpers.pyrohelper import get_arg
from config import PREFIX
from Prime import CMD_HELP, app


CMD_HELP.update(
    {
        "other": f"""
『 **Other** 』
  `{PREFIX}q` -> Membuat quotly.
  `{PREFIX}q` <warna> -> untuk merubah warna background.
  `{PREFIX}sg` -> Cek nama yang pernah di pakai.
  `{PREFIX}limit` -> Cek limit akun.
  `{PREFIX}json` -> Json.
  `{PREFIX}tt` -> Unduh video tik tok lewat link.
"""
    }
)


warna = ("red", "lime", "green", "blue", "cyan", "brown", "purple", "pink", "orange", "yellow", "white", "black")

@app.on_message(filters.command("q", PREFIX) & filters.me)
async def quotly(client, message):
    memek = get_arg(message)
    if not message.reply_to_message and not memek:
        await message.edit("Reply to any users text message")
        return
    bot = "QuotLyBot"
    chat = message.chat.id
    if message.reply_to_message:
        try:
            await message.edit("```Making a Quote```")

            await message.reply_to_message.forward(bot)
        except YouBlockedUser:
            await app.unblock_user(bot)
            await message.reply_to_message.forward(bot)
            
        await sleep(5)
        async for pepek in app.search_messages(bot, limit=1):
            if pepek:
                await message.delete()
                await message.reply_sticker(sticker=pepek.sticker.file_id,
                    reply_to_message_id=message.reply_to_message.id
                    if message.reply_to_message
                    else None,)
            else:
                return await message.edit_text("Sepertinya ada yang salah")
                
    elif memek in warna:
        await app.send_message(bot, f"/qcolor {memek}")
        await sleep(2)
        await message.edit(f"Berhasil merubah warna menjadi {memek}")
        return
    else:
        return await message.edit(f"Maaf tidak menemukan kode warna {memek}\nInilah kode warna yang ada\n{warna}")
        

@app.on_message(filters.command("limit", PREFIX) & filters.me)
async def limit(client, message):
    ppk = await message.edit_text("Processing")
    chat = message.chat.id
    bot = "SpamBot"
    try:
        tai = await app.send_message(bot, "/start")
        await tai.delete()
    except YouBlockedUser:
        await app.unblock_user(bot)
        tai = await app.send_message(bot, "/start")
        await tai.delete()
        
    async for jembut in app.get_chat_history(bot, limit=1):
        if not jembut:
            await message.edit_text("Sepertinya ada yang salah")
        elif jembut:
            oh = jembut.text
            await ppk.edit(oh)
            await jembut.delete()


@app.on_message(filters.command("json", PREFIX) & filters.me)
async def start(client, message):
    try:
        if message.reply_to_message:
            msg = message.reply_to_message
        else:
            msg = message

        msg_info = str(msg)

        if len(msg_info) > int("4096"):
            file = open("json.txt", "w+")
            file.write(msg_info)
            file.close()
            await app.send_document(
                message.chat.id,
                "json.txt",
                caption="Returned JSon",
            )
            remove("json.txt")

        else:
            await message.edit(msg_info)

    except Exception as e:
        await message.edit(f"{e}")

@app.on_message(filters.command(["sg", "sa"], PREFIX) & filters.me)
async def sangmata(client, message):
    await message.edit_text("Processing")
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await client.get_users(get_user)
    except PeerIdInvalid:
        await message.edit_text("Tidak menemukan user tersebut.")
        return
      
    bot = "SangMataInfo_bot"
    chat = message.chat.id
    if user:
        try:
            kon = await app.send_message(bot, f"/search_id {user.id}")
            await sleep(1)
            await kon.delete()
        except YouBlockedUser:
            await app.unblock_user(bot)
            kon = await app.send_message(bot, f"/search_id {user.id}")
            await sleep(1)
            await kon.delete()
    elif cmd[1]:
        try:
            kon = await app.send_message(bot, f"/search_id {cmd[1]}")
            await sleep(1)
            await kon.delete()
        except YouBlockedUser:
            await app.unblock_user(bot)
            kon = await app.send_message(bot, f"/search_id {cmd[1]}")
            await sleep(1)
            await kon.delete()
    async for jembut in app.search_messages(bot, query="Name", limit=1):
        if not jembut:
            await message.edit_text("Tidak menemukan riwayat nama target")
            return
        elif jembut:
            iss = jembut.text
            await kon.delete()
            await message.edit(iss)
            await jembut.delete()
            
            
@app.on_message(filters.command("tt", PREFIX) & filters.me)
async def sosmed(client, message):
    if len(message.command) < 2:
        return await message.edit(f"Format salah silahkan seperti contoh {PREFIX}tt link")
        
    await message.edit("Sedang memproses link")
    tetek = get_arg(message)
    try:
        url = requests.get(f"https://api.douyin.wtf/api?url={tetek}").json()
        tai = url.get("nwm_video_url", None)
        await app.send_video(message.chat.id, video=tai, caption=f"**Upload by :** {message.from_user.mention}")
        await message.delete()
    except Exception as e:
        await message.edit(f"**Error :** {e}")
