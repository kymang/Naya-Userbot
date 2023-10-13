# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
#
# All rights reserved.

# credit @tofik_dn @kenkan


from random import choice
import asyncio
from pyrogram import filters, enums
from Prime import CMD_HELP, app
from config import PREFIX
from Prime.helpers.pyrohelper import get_arg
from pyrogram.errors import YouBlockedUser


CMD_HELP.update(
    {
        "asupan": f"""
『 **Asupan** 』
  `{PREFIX}asupan` -> Dapatkan video asupan random.
  `{PREFIX}phub` -> Dapatkan video bokep random.
  `{PREFIX}desah` -> Dapatkan voice desahan random.
  `{PREFIX}logo` nama logo -> Dapatkan random generate logo.
"""
    }
)

OJO = [-1001347414136, -1001578091827]

@app.on_message(filters.command("asupan", PREFIX) & filters.me)
async def asupan(client, message):
    ppk = await message.edit("Sedang mencari video Asupan...")
    pop = message.from_user.first_name
    ah = message.from_user.id
    await message.reply_video(
        choice(
            [
                lol.video.file_id
                async for lol in app.search_messages("punyakenkan", filter=enums.MessagesFilter.VIDEO)
            ]
        ),
        False,
        caption=f"Nih kak [{pop}](tg://user?id={ah}) Video Asupannya"
    )

    await ppk.delete()

@app.on_message(filters.command("phub", PREFIX) & filters.me)
async def phub(client, message):
    ppk = await message.edit("Sedang mencari video bokep...")
    chat = message.chat.id
    if chat in OJO:
        await ppk.edit("**Maaf perintah ini dilarang di sini**")
        return
    elif chat not in OJO:
        await app.send_video(chat, 
        choice(
            [
                lol.video.file_id
                async for lol in app.search_messages("fakyudurov", filter=enums.MessagesFilter.VIDEO)
            ]
        ),
        False,
    )

    await ppk.delete()

@app.on_message(filters.command("desah", PREFIX) & filters.me)
async def desah(client, message):
    ppk = await message.edit("`Sedang mencari voice desah...`")
    chat = message.chat.id
    if chat in OJO:
        await ppk.edit("**Maaf perintah ini dilarang di sini**")
        return
    elif chat not in OJO:
        await app.send_voice(chat, 
        choice(
            [
                lol.voice.file_id
                async for lol in app.search_messages("punyakenkan", filter=enums.MessagesFilter.VOICE_NOTE)
            ]
        ),
        False,
    )

    await ppk.delete()


@app.on_message(filters.command("logo", PREFIX) & filters.me)
async def logo(client, message):
    tod = await message.edit_text("`Memproses logo...`")
    chat = message.chat.id
    jembut = get_arg(message)
    pop = message.from_user.first_name
    ah = message.from_user.id
    bot = "PrimeMegaBot"
    if jembut:
        try:
            kk = await app.send_message(bot, f"/logo {jembut}")
            await asyncio.sleep(10)
        except YouBlockedUser:
            await app.unblock_user(bot)
            kk = await app.send_message(bot, f"/logo {jembut}")
            await asyncio.sleep(10)
           
        async for lol in app.search_messages(bot, filter=enums.MessagesFilter.PHOTO, limit=1):
            if lol:
                await app.send_photo(
                    chat,
                    photo=lol.photo.file_id,
                    caption=f"**Logo by:** [{pop}](tg://user?id={ah})",
                )
                await tod.delete()
                await kk.delete()
                await lol.delete()
            else:
                await app.send_message(chat, "**Maaf ada yang salah**")
                await tod.delete()
    elif jembut:
        return await tod.edit("`Silahkan masukan nama logo`")
