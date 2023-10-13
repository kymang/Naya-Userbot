# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

import os
from pyrogram import filters
import asyncio
import Prime.database.pmpermitdb as Primedb
from config import PREFIX
from Prime import CMD_HELP, app
from Prime.helpers.pyrohelper import denied_users, get_arg

CMD_HELP.update(
    {
        "pmpermit": f"""
『 **Anti-PM** 』
  `{PREFIX}pmguard` [on or off] -> Mengaktifkan atau menonaktifkan anti-pm.
  `{PREFIX}setpmmsg` [message or default] -> Menyetel pesan anti-pm khusus.
  `{PREFIX}setblockmsg` [message or default] -> Menyetel pesan blokir khusus.
  `{PREFIX}setlimit` [value] -> Yang ini menetapkan maks. batas pesan untuk PM yang tidak diinginkan dan ketika mereka melampauinya, bamm!.
  `{PREFIX}allow` or `{PREFIX}a` -> Memungkinkan pengguna untuk PM Anda.
  `{PREFIX}deny` or `{PREFIX}d` -> Menolak pengguna untuk PM Anda.
  """
    }
)

FLOOD_CTRL = 0
ALLOWED = []
USERS_AND_WARNS = {}
PM_LOGO = os.environ.get("PM_LOGO")

@app.on_message(filters.command("pmguard", PREFIX) & filters.me)
async def pmguard(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**Saya hanya mengerti on atau off**")
        return
    if arg == "off":
        await Primedb.set_pm(False)
        await message.edit("**PM Guard Dinonaktifkan**")
    if arg == "on":
        await Primedb.set_pm(True)
        await message.edit("**PM Guard Diaktifkan**")


@app.on_message(filters.command("setlimit", PREFIX) & filters.me)
async def pmguard(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**Tetapkan batas untuk apa?**")
        return
    await Primedb.set_limit(int(arg))
    await message.edit(f"**Batas disetel ke {arg}**")
    
@app.on_message(filters.command("setpmmsg", PREFIX) & filters.me)
async def setpmmsg(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**Pesan apa yang akan disetel**")
        return
    if arg == "default":
        await Primedb.set_permit_message(Primedb.PMPERMIT_MESSAGE)
        await message.edit("**Pesan Anti-PM disetel ke default**.")
        return
    await Primedb.set_permit_message(f"{arg}")
    await message.edit("**Set pesan Anti-PM khusus**")


@app.on_message(filters.command("setblockmsg", PREFIX) & filters.me)
async def setpmmsg(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**Pesan apa yang akan disetel**")
        return
    if arg == "default":
        await Primedb.set_block_message(Primedb.BLOCKED)
        await message.edit("**Blokir pesan disetel ke default**.")
        return
    await Primedb.set_block_message(f"{arg}")
    await message.edit("**Set pesan blokir khusus**")


@app.on_message(filters.command(["allow", "a"], PREFIX) & filters.me & filters.private)
async def allow(client, message):
    chat_id = message.chat.id
    pmpermit, pm_message, limit, block_message = await Primedb.get_pm_settings()
    await Primedb.allow_user(chat_id)
    await message.edit(f"**Saya telah mengizinkan [Anda](tg://user?id={chat_id}) untuk PM saya.**")
    async for message in app.search_messages(
        chat_id=message.chat.id, query=pm_message, limit=1, from_user="me"
    ):
        await message.delete()
    USERS_AND_WARNS.update({chat_id: 0})


@app.on_message(filters.command(["deny", "d"], PREFIX) & filters.me & filters.private)
async def deny(client, message):
    chat_id = message.chat.id
    await Primedb.deny_user(chat_id)
    await message.edit(f"**Saya telah menolak [Anda](tg://user?id={chat_id}) untuk PM saya.**")


@app.on_message(
    filters.private
    & filters.create(denied_users)
    & filters.incoming
    & ~filters.service
    & ~filters.me
    & ~filters.bot
)
async def reply_pm(client, message):
    global FLOOD_CTRL
    pmpermit, pm_message, limit, block_message = await Primedb.get_pm_settings()
    user = message.from_user.id
    user_warns = 0 if user not in USERS_AND_WARNS else USERS_AND_WARNS[user]
    if user_warns <= limit - 2:
        user_warns += 1
        USERS_AND_WARNS.update({user: user_warns})
        if not FLOOD_CTRL > 0:
            FLOOD_CTRL += 1
        else:
            FLOOD_CTRL = 0
            return
        async for message in app.search_messages(
            chat_id=message.chat.id, query=pm_message, limit=1, from_user="me"
        ):
            await message.delete()
        if not PM_LOGO:
            await message.reply(pm_message, disable_web_page_preview=True)
        else:
            ahh = app.send_video if PM_LOGO.endswith(".mp4") else app.send_photo
            await asyncio.gather(
                    ahh(
                        message.chat.id,
                        PM_LOGO,
                        caption=pm_message
                    ),
                )
            return
    await message.reply(block_message, disable_web_page_preview=True)
    await app.block_user(message.chat.id)
    USERS_AND_WARNS.update({user: 0})
