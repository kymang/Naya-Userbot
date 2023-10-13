# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

from pyrogram import filters

import Prime.database.welcomedb as Primedb
from config import LOG_CHAT, PREFIX
from Prime import CMD_HELP, app
from Prime.helpers.pyrohelper import welcome_chat

CMD_HELP.update(
    {
        "welcome": f"""
『 **Greetings** 』
  `{PREFIX}setwelcome` -> Menyetel pesan selamat datang.
  `{PREFIX}clearwelcome` -> Menonaktifkan pesan selamat datang dalam obrolan.
    """
    }
)

LOG_CHAT = LOG_CHAT


@app.on_message(filters.command("clearwelcome", PREFIX) & filters.me)
async def welcome(client, message):
    await Primedb.clear_welcome(str(message.chat.id))
    await message.edit("Saya merajuk untuk tidak menyapa lagi :(**" )



@app.on_message(filters.create(welcome_chat) & filters.new_chat_members, group=-2)
async def new_welcome(client, message):
    msg_id = await Primedb.get_welcome(str(message.chat.id))
    caption = ""
    men = ""
    msg = await app.get_messages(LOG_CHAT, msg_id)
    if msg.media:
        if msg.caption:
            caption = msg.caption
            if "{mention}" in caption:
                men = caption.replace("{mention}", "[{}](tg://user?id={})")
        if msg.photo and caption is not None:
            await app.send_photo(
                message.chat.id,
                msg.photo.file_id,
                caption=men.format(
                    message.new_chat_members[0]["first_name"],
                    message.new_chat_members[0]["id"],
                ),
                reply_to_message_id=message.id,
            )
        if msg.animation and caption is not None:
            await app.send_animation(
                message.chat.id,
                msg.animation.file_id,
                caption=men.format(
                    message.new_chat_members[0]["first_name"],
                    message.new_chat_members[0]["id"],
                ),
                reply_to_message_id=message.id,
            )
        if msg.sticker:
            await app.send_sticker(
                message.chat.id,
                msg.sticker.file_id,
                reply_to_message_id=message.id,
            )

    else:
        text = msg.text
        if "{mention}" in text:
            men = text.replace("{mention}", "[{}](tg://user?id={})")
            await app.send_message(
                message.chat.id,
                men.format(
                    message.new_chat_members[0]["first_name"],
                    message.new_chat_members[0]["id"],
                ),
                reply_to_message_id=message.id,
            )
        else:
            await app.send_message(
                message.chat.id, text, reply_to_message_id=message.id
            )


@app.on_message(filters.command("setwelcome", PREFIX) & filters.me)
async def setwelcome(client, message):
    reply = message.reply_to_message
    if not reply:
        await message.edit("**Balas pesan atau media untuk mengatur pesan selamat datang.**")
        return
    frwd = await app.copy_message(LOG_CHAT, message.chat.id, reply.id)
    msg_id = frwd.id
    await Primedb.save_welcome(str(message.chat.id), msg_id)
    await message.edit("**Pesan selamat datang telah disimpan.**")
