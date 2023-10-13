# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

import os

from pyrogram import filters, Client
from removebg import RemoveBg
from pyrogram.types import *

from Prime.helpers.pyrohelper import ReplyCheck
from Prime import app, CMD_HELP
from config import *

RMBG_API = os.environ.get("RMBG_API", "a6qxsmMJ3CsNo7HyxuKGsP1o")

DOWN_PATH = 'Primesku/'

IMG_PATH = DOWN_PATH + "primes.jpg"


@app.on_message(filters.me & filters.command(["rmbg"], PREFIX))
async def remove_bg(client, message):
    if not RMBG_API:
        await message.edit("Get the API from [Remove.bg](https://www.remove.bg/b/background-removal-api)",
                           disable_web_page_preview=True, parse_mode="html")
    await message.edit("Analysing...")
    replied = message.reply_to_message
    if (replied and replied.media
            and (replied.photo
                 or (replied.document and "image" in replied.document.mime_type))):
        if os.path.exists(IMG_PATH):
            os.remove(IMG_PATH)
        await client.download_media(message=replied, file_name=IMG_PATH)
        await message.edit("Menghapus backgroundnya...")
        try:
            rmbg = RemoveBg(RMBG_API, "rm_bg_error.log")
            rmbg.remove_background_from_img_file(IMG_PATH)
            remove_img = IMG_PATH + "_no_bg.png"
            await client.send_document(
                chat_id=message.chat.id,
                document=remove_img,
                reply_to_message_id=ReplyCheck(message),
                disable_notification=True)
            await message.delete()
        except Exception as e:
            print(e)
            await message.edit("Telah terjadi suatu kesalahan!.")
    else:
        await message.edit("Usage: Mohon reply ke gambar yang ingin dihapus backgroundnya!")
        
 
@app.on_message(filters.command("dm", PREFIX) & filters.me)
async def dmm(client, message):
    if len(message.command) < 3:
        return await message.edit(f"`{PREFIX}dm` username atau id isi pesan\nContoh : `{PREFIX}dm @username Salken`")
    user = message.command[1]
    split = message.command[2:]
    pesan = " ".join(split)
    await app.send_message(user, pesan)
    await message.edit("Berhasil mengirim pesan")
        
CMD_HELP.update(
  {
    "remove": f"""
『 **Remove Background** 』
`{PREFIX}rmbg` -> Reply ke gambar yang ingin dihapus background nya
"""
  }
)

CMD_HELP.update(
  {
    "dm": f"""
『 **DM** 』
`{PREFIX}dm` -> Kirim pesan ke seseorang
"""
  }
)
