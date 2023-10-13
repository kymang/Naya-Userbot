# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

import wikipedia

from pyrogram import filters
from Prime import app, CMD_HELP
from config import PREFIX

@app.on_message(filters.command("wiki", PREFIX) & filters.me)
async def wiki(client, message):
    lang = message.command[1]
    user_request = " ".join(message.command[2:])
    await message.edit("**Telusuri info**")
    if user_request == "":
        wikipedia.set_lang("id")
        user_request = " ".join(message.command[1:])
    try:
        if lang == "id":
            wikipedia.set_lang("id")

        result = wikipedia.summary(user_request)
        await message.edit(
            f"""**Kata:**
`{user_request}`
**Info:**
`{result}`"""
        )
    except Exception as exc:
        await message.edit(
            f"""**Request:**
`{user_request}`
**Result:**
`{exc}`"""
        )
        
CMD_HELP.update(
  {
    "wiki": f"""
『 **Wikipedia** 』
`{PREFIX}wiki [Kata] -> Mencari kata di wikipedia
"""
  }
)
