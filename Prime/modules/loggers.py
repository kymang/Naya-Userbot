# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

# yukki
# abdul
# kenkan

import os
from pyrogram import filters
from config import LOG_CHAT, PREFIX
from Prime import CMD_HELP, app
from Prime.database.logdb import is_pmlogs, is_gruplogs, add_on, add_off, addg_on, addg_off
from Prime.helpers.pyrohelper import get_arg

CMD_HELP.update(
    {
        "loggs": f"""
『 **Loggs** 』
  `{PREFIX}pmlog` [on atau off] -> Untuk logs pm.
  `{PREFIX}gruplog` [on atau off] -> Untuk logs group.
"""
    }
)
PMLOG = 2
GRUPLOG = 2

@app.on_message(filters.command("pmlog", PREFIX) & filters.me)
async def pmlogs(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**Saya hanya mengerti on atau off**")
        return
    if arg == "off":
        await add_off(PMLOG)
        await message.edit("**PM Log Dinonaktifkan**")
    if arg == "on":
        await add_on(PMLOG)
        await message.edit("**PM Log Diaktifkan**")

@app.on_message(filters.command("gruplog", PREFIX) & filters.me)
async def gruplogs(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**Saya hanya mengerti on atau off**")
        return
    if arg == "off":
        await addg_off(GRUPLOG)
        await message.edit("**Grup Log Dinonaktifkan**")
    if arg == "on":
        await addg_on(GRUPLOG)
        await message.edit("**Grup Log Diaktifkan**")


@app.on_message(
    filters.private
    & filters.incoming
    & ~filters.service
    & ~filters.me
    & ~filters.bot
)
async def pmlogchat(client, message):
    if await is_pmlogs(PMLOG):
        chat = message.chat.id
        async for pepek in app.search_messages(chat, limit=1):
            if chat != 777000:
                await pepek.forward(LOG_CHAT)
        
@app.on_message(filters.group & filters.mentioned & filters.incoming)
async def grouplogchat(client, message):
    if await is_gruplogs(GRUPLOG):
        await app.send_message(LOG_CHAT,
f"""✅ **GRUP LOG  MENTION**
🧑‍💼 **Dari :** {message.from_user.mention}
💬 **Pesan:** [{message.text}]({message.link})
             """,
             disable_web_page_preview=True)
        
