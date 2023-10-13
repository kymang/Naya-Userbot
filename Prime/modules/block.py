# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

from pyrogram import filters
from pyrogram.errors import RPCError
from Prime import CMD_HELP, app
from config import PREFIX


CMD_HELP.update(
  {
    "block": f"""
『 **Blockir** 』
  `{PREFIX}block` bales user -> Block user.
  `{PREFIX}unblock` bales user -> Unblock user.
  """
  }
)


@app.on_message(filters.command("block", PREFIX) & filters.me)
async def blockir(client, message):
    cmd = message.command
    chat_id = message.chat.id
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = cmd[1]
        except RPCError:
            pass
    try:
        user = await client.get_users(get_user)
    except RPCError:
        await message.edit("Tidak menemukan user tersebut.")
        return
    await app.block_user(user.id)
    await message.edit(f"**{user.mention} Telah di blockir**")


@app.on_message(filters.command("unblock", PREFIX) & filters.me)
async def unblockir(client, message):
    cmd = message.command
    chat_id = message.chat.id
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = cmd[1]
        except RPCError:
            pass
    try:
        user = await client.get_users(get_user)
    except RPCError:
        await message.edit("Tidak menemukan user tersebut.")
        return
    await app.unblock_user(user.id)
    await message.edit(f"**{user.mention} Telah di unblockir**")
