# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
# Aryazakaria
# All rights reserved.



from pyrogram import __version__ as pyver
from pyrogram import idle
import heroku3
from pyrogram.errors import BadRequest
from config import PREFIX, LOG_CHAT, HEROKU_API, HEROKU_APP_NAME
from Prime import app
from Prime.modules import *

app.start()
me = app.get_me()

print(
    f"Prime UserBot started for user {me.first_name}. Type {PREFIX}help in any telegram chat."
)
try:
    if not str(LOG_CHAT).startswith("-100"):
        tai = app.create_supergroup("Prime-Logs", "Powered by : @PrimeSupportGroup\nPatner : @kenkanasw")
        app.set_chat_photo(tai.id, photo="Prime/sampah/prime.png")
        Heroku = heroku3.from_key(HEROKU_API)
        her = Heroku.app(HEROKU_APP_NAME)
        heroku_var = her.config()
        heroku_var["LOG_CHAT"] = tai.id
    else:
        print("LOG_CHAT, Sudah benar")
    app.send_message(
        LOG_CHAT,
        f"🔥 **𝗣𝗿𝗶𝗺𝗲-𝗨𝘀𝗲𝗿𝗕𝗼𝘁 𝘂𝗱𝗮𝗵 𝗡𝘆𝗮𝗹𝗮 𝗔𝗻𝗷𝗮𝘆𝘆** 🔥\n└ •**ᴏᴡɴᴇʀ** : [{me.first_name}](tg://user?id={me.id})\n└ •**ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ :** `{pyver}`\n└ •**ᴘʀɪᴍᴇ ᴠᴇʀsɪᴏɴ  :** `3.2.1`\n└ •**sᴜᴘᴘᴏʀᴛ ʙʏ :** @PrimeSupportGroup\n└ •**ᴘᴀʀᴛɴᴇʀ :** @kenkanasw\n\n**Gunakan** `{PREFIX}ping` **untuk cek bot aktif**"
    )
    app.join_chat("PrimeSupportGroup")
    app.join_chat("PrimeSupportChannel")
    app.join_chat("aruna_mutual")
    app.join_chat("gabutan_escape")
    
    idle()
except BadRequest:
    pass
