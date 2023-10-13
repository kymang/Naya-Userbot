# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.


import asyncio
import time

from pyrogram import filters

import Prime.database.afkdb as Prime
from config import LOG_CHAT, PREFIX
from Prime import CMD_HELP, app
from Prime.helpers.pyrohelper import get_arg, user_afk
from Prime.helpers.utils import Types, get_message_type
from Prime.modules.alive import get_readable_time

CMD_HELP.update(
    {
        "afk": f"""
『 **AFK** 』
  `{PREFIX}afk [reason]` -> Memberikan pesan yang mengatakan bahwa Anda off.
  `{PREFIX}unafk` -> Hapus status AFK.
"""
    }
)

LOG_CHAT = LOG_CHAT

MENTIONED = []
AFK_RESTIRECT = {}
DELAY_TIME = 60


@app.on_message(filters.command("afk", PREFIX) & filters.me)
async def afk(client, message):
    afk_time = int(time.time())
    arg = get_arg(message)
    if not arg:
        reason = None
    else:
        reason = arg
    await Prime.set_afk(True, afk_time, reason)
    await message.edit("**⚆ _ ⚆ Aɴᴊᴀʏ Gᴜᴇ Cᴀʙᴜᴛ ᴅᴜʟᴜ ʏᴇᴇᴇ **")


@app.on_message(filters.mentioned & ~filters.bot & filters.create(user_afk), group=11)
async def afk_mentioned(_, message):
    global MENTIONED
    afk_time, reason = await Prime.afk_stuff()
    afk_since = get_readable_time(time.time() - afk_time)
    if "-" in str(message.chat.id):
        cid = str(message.chat.id)[4:]
    else:
        cid = str(message.chat.id)

    if cid in list(AFK_RESTIRECT) and int(AFK_RESTIRECT[cid]) >= int(time.time()):
        return
    AFK_RESTIRECT[cid] = int(time.time()) + DELAY_TIME
    if reason:
        await message.reply(
            f"**Gᴡᴇʜʜ AFK Jᴇᴍʙᴜᴜᴛ (since {afk_since})\nAʟᴇsᴀɴ »** __{reason}__"
        )
    else:
        await message.reply(f"**◈ ━━━━━━━ ⸙ Gᴜᴇ AFK Cᴏᴋ ⸙ ━━━━━━━ ◈ (since {afk_since})**")

        _, message_type = get_message_type(message)
        if message_type == Types.TEXT:
            text = message.text or message.caption
        else:
            text = message_type.name

        MENTIONED.append(
            {
                "user": message.from_user.first_name,
                "user_id": message.from_user.id,
                "chat": message.chat.title,
                "chat_id": cid,
                "text": text,
                "message_id": message.id,
            }
        )


@app.on_message(filters.create(user_afk) & filters.outgoing)
async def auto_unafk(_, message):
    await Prime.set_unafk()
    unafk_message = await app.send_message(message.chat.id, "**✦✧✧ ɥǝɥsɐꟽ ʞᴉlɐᗺ ǝn⅁ ✧✧✦**")
    global MENTIONED
    text = "**ıllıllı 𝗧𝗼𝘁𝗮𝗹 {} 𝗬𝗮𝗻𝗴 𝗸𝗮𝗻𝗴𝗲𝗻 𝗲𝗻𝘁𝗲 ıllıllı**\n".format(len(MENTIONED))
    for x in MENTIONED:
        msg_text = x["text"]
        if len(msg_text) >= 11:
            msg_text = "{}...".format(x["text"])
        text += "- [{}](https://t.me/c/{}/{}) ({}): {}\n".format(
            x["user"],
            x["chat_id"],
            x["message_id"],
            x["chat"],
            msg_text,
        )
        await app.send_message(LOG_CHAT, text)
        MENTIONED = []
    await asyncio.sleep(2)
    await unafk_message.delete()
