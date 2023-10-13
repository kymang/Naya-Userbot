# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

from asyncio import sleep
from pyrogram import filters
from Prime import CMD_HELP, app
from config import PREFIX
from Prime.helpers.pyrohelper import get_arg


CMD_HELP.update(
    {
        "tagall": f"""
『 **Tagall** 』
  `{PREFIX}tagall` [text] -> Mention semua member group.
  `{PREFIX}cancel` -> Batalkan tagall.
"""
    }
)

spam_chats = []

@app.on_message(filters.command("tagall", PREFIX) & filters.me)
async def mentionall(client, message):
    await message.delete()
    chat_id = message.chat.id
    tai = message.reply_to_message
    ppk = get_arg(message)
    if not tai and not ppk:
        return await message.edit("__Tolong berikan saya pesan atau balas ke pesan!__")

    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ''
    async for usr in app.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}), "
        if usrnum == 5:
            if ppk:
                txt = f"{ppk}\n{usrtxt}"
                await app.send_message(chat_id, txt)
            elif tai:
                await tai.reply(usrtxt)
            await sleep(2)
            usrnum = 0
            usrtxt = ''
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@app.on_message(filters.command("cancel", PREFIX) & filters.me)
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.edit("__Sepertinya tidak ada tagall disini...__")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.edit("__Stopped Mention.__")

