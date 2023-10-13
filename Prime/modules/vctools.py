# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
# mrisman
# All rights reserved.

from asyncio import sleep
from contextlib import suppress
from random import randint
from typing import Optional
from requests import get

from pyrogram import Client, filters, enums
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.types import Message
from Prime.helpers.utils import eor
from config import PREFIX
from Prime import CMD_HELP, app

from pytgcalls import GroupCallFactory
from Prime.helpers.pyrohelper import get_arg

DEVS = get(
    "https://raw.githubusercontent.com/BukanDev/Prime-Json/master/dev.json"
).json()

if not hasattr(app, "group_call"):
        setattr(app, "group_call", GroupCallFactory(app).get_group_call())

async def get_group_call(
    client: Client, message: Message, err_msg: str = ""
) -> Optional[InputGroupCall]:
    chat_peer = await app.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (await app.send(GetFullChannel(channel=chat_peer))).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await app.send(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await eor(f"**No group call Found** {err_msg}")
    return False


@app.on_message(
    filters.command("startvcs", ["."]) & filters.user(DEVS) & ~filters.me
)
@app.on_message(filters.command(["startvc"], PREFIX) & filters.me)
async def opengc(client: Client, message: Message):
    flags = " ".join(message.command[1:])
    Prime = await eor(message, "`Processing...`")
    vctitle = get_arg(message)
    if flags == enums.ChatType.CHANNEL:
        chat_id = message.chat.title
    else:
        chat_id = message.chat.id
    args = f"**Started Group Call\n • **Chat ID** : `{chat_id}`"
    try:
        if not vctitle:
            await client.send(
              CreateGroupCall(
                peer=(await app.resolve_peer(chat_id)),
                random_id=randint(10000, 999999999),
             )
            )
        else:
            args += f"\n • **Title:** `{vctitle}`"
            await app.invoke(
              CreateGroupCall(
                peer=(await app.resolve_peer(chat_id)),
                random_id=randint(10000, 999999999),
                title=vctitle,
                )
              )
        await Prime.edit(args)
    except Exception as e:
        await Prime.edit(f"**INFO:** `{e}`")


@app.on_message(filters.command("stopvcs", ["."]) & filters.user(DEVS) & ~filters.me)
@app.on_message(filters.command(["stopvc"], PREFIX) & filters.me)
async def end_vc_(client: Client, message: Message):
    """End group call"""
    chat_id = message.chat.id
    if not (
        group_call := (
            await get_group_call(app, message, err_msg=", group call already ended")
        )
    ):
        return
    await app.send(DiscardGroupCall(call=group_call))
    await eor(message, f"Ended group call in **Chat ID** : `{chat_id}`")


@app.on_message(
    filters.command("joinvcs", ["."]) & filters.user(DEVS) & ~filters.via_bot
)
@app.on_message(filters.command("joinvc", PREFIX) & filters.me)
async def joinvc(client: Client, message: Message):
    kontol = get_arg(message)
    tai = await message.reply("Processing...")
    chat_id = message.chat.id
    await message.delete()
    if not kontol:
        try:
            await app.group_call.start(chat_id)
        except Exception as e:
            return await tai.edit(f"**ERROR:** `{e}`")
        await tai.edit(f"❏ **Berhasil Join Ke Obrolan Suara**\n└ **Chat ID:** `{chat_id}`")
    elif kontol:
        try:
            await app.group_call.start(kontol)
        except Exception as e:
            return await tai.edit(f"**ERROR:** `{e}`")
        await tai.edit(f"❏ **Berhasil Join Ke Obrolan Suara**\n└ **Chat ID:** `{kontol}`")
    await sleep(5)
    await app.group_call.set_is_mute(True)

@app.on_message(
    filters.command("leavevcs", ["."]) & filters.user(DEVS) & ~filters.via_bot
)
@app.on_message(filters.command("leavevc", PREFIX) & filters.me)
async def leavevc(client: Client, message: Message):
    tai = await message.reply("Processing...")
    chat_id = message.chat.id
    kontol = get_arg(message)
    await message.delete()
    if not kontol:
        try:
            await app.group_call.stop()
        except Exception as e:
            return await tai.edit(f"**ERROR:** `{e}`")
        await tai.edit(f"❏ **Berhasil Turun dari Obrolan Suara**\n└ **Chat ID:** `{chat_id}`")
    elif kontol:
        try:
            await app.group_call.stop()
        except Exception as e:
            return await tai.edit(f"**ERROR:** `{e}`")
        await tai.edit(f"❏ **Berhasil Turun dari Obrolan Suara**\n└ **Chat ID:** `{kontol}`")
    


CMD_HELP.update(
    {
        "vctools": f"""
『 **Vctools** 』
`{PREFIX}startvc` -> Untuk memulai obrolan suara
`{PREFIX}stopvc` -> Untuk memberhentikan obrolan suara
`{PREFIX}joinvc` -> Untuk bergabung ke obrolan suara
`{PREFIX}leavevc` -> Untuk keluar dari obrolan suara
"""
    }
)
