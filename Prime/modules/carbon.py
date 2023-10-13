# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

from io import BytesIO

from pyrogram import Client, filters
from pyrogram.types import Message
from aiohttp import ClientSession
from config import PREFIX
from Prime import app, CMD_HELP
from Prime.helpers.utils import eor

aiosession = ClientSession()

async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


@app.on_message(filters.command("carbon", PREFIX) & filters.me)
async def carbon_func(client, message):
    text = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    if not text:
        return await message.delete()
    Prime = await eor(message, "`Preparing Carbon...`")
    carbon = await make_carbon(text)
    await Prime.edit("`Uploading...`")
    ah = await app.get_me()
    await app.send_photo(
        message.chat.id,
        carbon,
        caption=f"**Carbonised by** {ah.mention}",
    )
    await Prime.delete()
    carbon.close()
    
CMD_HELP.update(
  {
    "carbon": f"""
『 **Carbon** 』
`{PREFIX}carbon` [Reply] -> Carbonisasi teks dengan pengaturan default.
"""
  }
)
