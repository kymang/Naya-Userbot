# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.
import heroku3
import asyncio
import os
from os import getenv
from pyrogram import filters, enums
from requests import get
from config import PREFIX, HEROKU_APP_NAME, HEROKU_API
from Prime import CMD_HELP, app
from Prime.helpers.pyrohelper import get_arg

CMD_HELP.update(
    {
        "gcast": f"""
『 **Broadcast** 』
  `{PREFIX}gcast` -> Kirim pesan ke group.
  `{PREFIX}gucast` -> Kirim pesan ke private.
  `{PREFIX}blcht` -> Untuk melihat daftar blacklist gcast
  `{PREFIX}addbl` -> Untuk menambahkan grup ke dalam blacklist gcast
  `{PREFIX}delbl` -> Untuk menghapus grup dari blacklist gcast
"""
    }
)

BL = get(
    "https://raw.githubusercontent.com/BukanDev/Prime-Json/master/blgcast.json"
).json()
BLACKLIST_GCAST = {int(x) for x in os.getenv
                  ("BLACKLIST_GCAST", "").split()}

Heroku = heroku3.from_key(HEROKU_API)
heroku_api = "https://api.heroku.com"
blchat = getenv("BLACKLIST_GCAST") or ""

@app.on_message(filters.command("gcast", PREFIX) & filters.me)
async def chat_broadcast(client, message):
    if message.reply_to_message:
        msg = message.reply_to_message
    else:
        await message.edit_text("Reply to a message to broadcast it")
        return
    await message.edit("Sedang mengirimkan gcast")
    sent = 0
    failed = 0
    async for dialog in app.get_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [
            enums.ChatType.GROUP,
            enums.ChatType.SUPERGROUP,
        ]:
            chat = dialog.chat.id
            if chat not in BL and chat not in BLACKLIST_GCAST:
                try:
                    await msg.copy(chat)
                    sent = sent + 1
                    await asyncio.sleep(0.1)
                except:
                    failed = failed + 1
                    await asyncio.sleep(0.1)

    return await message.edit_text(
        f"**Pesan global selesai \n\nTerkirim ke:** `{sent}` **Chats \nGagal terkirim ke:** `{failed}` **Chats**"
    )


@app.on_message(filters.command("gucast", PREFIX) & filters.me)
async def chat_broadcast(client, message):
    if message.reply_to_message:
        msg = message.reply_to_message
    else:
        await message.edit_text("Reply to a message to broadcast it")
        return
    await message.edit("Sedang mengirimkan gcast")
    sent = 0
    failed = 0
    async for dialog in app.get_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [
            enums.ChatType.PRIVATE
            ]:
            chat = dialog.chat.id
            try:
                await msg.copy(chat)
                sent = sent + 1
                await asyncio.sleep(0.1)
            except:
                failed = failed + 1
                await asyncio.sleep(0.1)

    return await message.edit_text(
        f"**Pesan global selesai \n\nTerkirim ke:** `{sent}` **Chats \nGagal terkirim ke:** `{failed}` **Chats**"
    )

@app.on_message(filters.command("addbl", PREFIX) & filters.me)
async def add(client, message):
    jmbt = await message.reply("Sedang memproses...")
    vars = "BLACKLIST_GCAST"
    grup = message.chat.id
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        await jmbt.edit(
            "**Silahkan Isi Var** `HEROKU_APP_NAME` **Untuk Menambahkan blacklist**",
        )
        return
    heroku_Config = app.config()
    if message is None:
       return
    blgc = f"{BLACKLIST_GCAST} {grup}"
    blacklistgrup = (
        blgc.replace("{", "")
        .replace("}", "")
        .replace(",", "")
        .replace("[", "")
        .replace("]", "")
        .replace("set() ", "")
    )
    await jmbt.edit(
        f"**Berhasil Menambahkan** `{grup}` **ke daftar blacklist gcast.**\n\nSedang MeRestart Heroku untuk menerapkan perubahan."
    )
    heroku_Config[vars] = blacklistgrup

@app.on_message(filters.command("blcht", PREFIX) & filters.me)
async def gcast_bl(client, message):
    blacklistgc = "True" if BLACKLIST_GCAST else "False"
    blc = blchat
    list = blc.replace(" ", "\n> ")
    if blacklistgc == "True":
        await message.reply(
            f"**Blacklist GCAST:** `Enable`\n\n**Blacklist Group:**\n> {list}\n\nKetik `{PREFIX}addbl` di grup yang ingin di tambahkan ke daftar blacklist.",
        )
    else:
        await message.reply("**Blacklist GCAST:** `Disable`")

@app.on_message(filters.command("delbl", PREFIX) & filters.me)
async def _(client, message):
    jmbt = await message.reply("`Sedang Memproses...`")
    gc = message.chat.id
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        await jmbt.edit(
            "**Silahkan Tambahkan Vars** `HEROKU_APP_NAME` **Untuk menghapus blacklist gcast**",
        )
        return
    heroku_Config = app.config()
    if message is None:
        return
    gett = str(gc)
    if gett in blchat:
        blacklistgrup = blchat.replace(gett, "")
        await jmbt.edit(
            f"**Berhasil Menghapus** `{gc}` **dari daftar blacklist gcast.**\n\nSedang MeRestart Heroku untuk menerapkan perubahan."
        )
        vars = "BLACKLIST_GCAST"
        heroku_Config[vars] = blacklistgrup
    else:
        await jmbt.edit(
            "**Grup ini tidak ada dalam daftar blacklist gcast.**"
        )
