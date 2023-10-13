# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

from pyrogram import filters
from pyrogram.types import Message


from config import PREFIX
from Prime import app, CMD_HELP
from Prime.helpers.utils import eor

CMD_HELP.update(
    {
        "buat": f"""
『 **Buat** 』
  `{PREFIX}buat b` Nama -> Membuat basic group.
  `{PREFIX}buat s` Nama -> Membuat supergroup.
  `{PREFIX}buat c` Nama -> Membuat channel.
"""
    }
)


@app.on_message(filters.command("buat", PREFIX) & filters.me)
async def create(client, message):
    if len(message.command) < 3:
        return await eor(message, text=f"__**{PREFIX}buat (b|s|c) Nama**__")
    group_type = message.command[1]
    split = message.command[2:]
    group_name = " ".join(split)
    desc = "Selamat Datang di" + (
        "Supergroup" if group_type == "s" else "Channel"
    )
    if group_type == "b":  # for basicgroup
        group = await app.create_group(group_name, "PrimeMegaBot")
        await eor(
            message,
            text=f"**Group dibuat: [{group_name}]({(await app.get_chat(group.id)).invite_link})**",
            disable_web_page_preview=True,
        )
    elif group_type == "s":  # for supergroup
        group = await app.create_supergroup(group_name, desc)
        await eor(
            message,
            text=f"**Supergroup dibuat: [{group_name}]({(await app.get_chat(group.id)).invite_link})**",
            disable_web_page_preview=True,
        )
    elif group_type == "c":  # for channel
        group = await app.create_channel(group_name, desc)
        await eor(
            message,
            text=f"**Channel dibuat: [{group_name}]({(await app.get_chat(group.id)).invite_link})**",
            disable_web_page_preview=True,
        )
