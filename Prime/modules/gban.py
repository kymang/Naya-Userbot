# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.


import asyncio
from pyrogram import filters, enums
from requests import get
from pyrogram.errors import PeerIdInvalid
from config import PREFIX
from Prime import CMD_HELP, app

CMD_HELP.update(
    {
        "gban": f"""
『 **Gban** 』
  `{PREFIX}gban` -> Melakukan global banned.
  `{PREFIX}ungban` - > Membatalkan global banned.
"""
    }
)

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

@app.on_message(filters.command("gban", PREFIX) & filters.me)
async def gban(client, message):
    kontol = await message.edit_text("Processing gban user")
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

    iso = 0
    gagal = 0
    prik = user.id
    async for dialog in app.get_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL]:
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
                except:
                    gagal = gagal + 1
                    await asyncio.sleep(0.1)

    return await kontol.edit(f"**Global Banned**\n\n**Terbanned :** {iso} Chats \n**Gagal Banned :** {gagal} Chats\n**Korban :** [{user.first_name}](tg://user?id={prik})\n**by : Prime-Userbot**"
    )


@app.on_message(filters.command("ungban", PREFIX) & filters.me)
async def ungban(client, message):
    kontol = await message.edit_text("Processing ungban user")
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

    iso = 0
    gagal = 0
    prik = user.id
    async for dialog in app.get_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL]:
            chat = dialog.chat.id
            if prik not in DEVS and prik not in WHITELIST:
                try:
                    await app.unban_chat_member(chat, prik)
                    iso = iso + 1
                    await asyncio.sleep(0.1)
                except:
                    gagal = gagal + 1
                    await asyncio.sleep(0.1)

    return await kontol.edit(f"**Global Ungbanned**\n\n**Ungbanned :** {iso} Chats \n**Gagal Ungbanned :** {gagal} Chats\n**Korban :** [{user.first_name}](tg://user?id={prik})\n**By : Prime-Userbot**"
        )
