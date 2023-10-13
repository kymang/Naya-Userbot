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
from telegraph import upload_file
from requests import get
from config import PREFIX
from Prime import CMD_HELP, app

CMD_HELP.update(
    {
        "telegraph": f"""
『 **Telegraph** 』
  `{PREFIX}tm` atau `{PREFIX}tgm` -> Upload media ke Telegraph.
"""
    }
)

@app.on_message(filters.command(["tm", "tgm"], PREFIX) & filters.me)
async def telegraph(client, message):
    replied = message.reply_to_message
    await message.edit("Processing")
    if not replied or replied.text:
        await message.edit_text("reply to a supported media file")
        return
    if replied.photo or replied.video:
        tgm = await app.download_media(
        message=message.reply_to_message, file_name="./downloads/")
        response = upload_file(tgm)
        await message.edit(f"**Document passed to: [Telegra.ph](https://telegra.ph{response[0]})**")
        os.remove(tgm)

@app.on_message(filters.command("qrd", PREFIX) & filters.me)
async def qrdecode(client, message):
    uh = await message.edit("Prosses membaca barcode")
    replied = message.reply_to_message
    if not replied:
        await uh.edit("reply to a supported media file")
        return
    if not (
        (replied.photo and replied.photo.file_size <= 5242880)
        or (
            replied.document
            and replied.document.file_name.endswith(
                (".jpg", ".jpeg", ".png")
            )
            and replied.document.file_size <= 5242880
        )
    ):
        await uh.edit("not supported!")
        return
    download_location = await app.download_media(
        message=message.reply_to_message, file_name="./downloads/"
        )
    try:
        response = upload_file(download_location)
    except Exception as document:
        await app.send_message(message.chat.id, document)
    else:
        ppk = f"https://telegra.ph{response[0]}"
        tai = get(f"http://api.qrserver.com/v1/read-qr-code/?fileurl={ppk}").json()
        memek = (tai[0]["symbol"][0]["data"])
        await uh.edit(memek)
    finally:
        os.remove(download_location)
