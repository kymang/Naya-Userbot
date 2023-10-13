# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

from pyrogram import filters, Client
from config import PREFIX
from Prime import app, CMD_HELP


@app.on_message(filters.command("qr", PREFIX) & filters.me)
async def qr(client, message):
    tono = await message.edit("Prosessing buat qr code....")
    texts = ""
    if message.reply_to_message:
        texts = message.reply_to_message.text
    elif len(message.text.split(maxsplit=1)) == 2:
        texts = message.text.split(maxsplit=1)[1]
    text = texts.replace(' ', '%20')
    QRcode = f"https://api.qrserver.com/v1/create-qr-code/?size=1020x1020&data={text}"
    await app.send_photo(
        message.chat.id, 
        QRcode,
        reply_to_message_id=message.reply_to_message.id
        if message.reply_to_message
        else None,)
    await tono.delete()
    
    
CMD_HELP.update(
  {
    "barcode": f"""
『 **Barcode** 』
  `{PREFIX}qr` [Text] -> Generate barcode.
  `{PREFIX}qrd` [photo qr] -> Baca barcode.
  """
  }
)
