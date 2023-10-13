# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.


import asyncio
from requests import get
from datetime import datetime
from inspect import getfullargspec
from pyrogram.errors import RPCError
from pyrogram import filters, enums
from pyrogram.types import Message
from config import PREFIX
from Prime import CMD_HELP, app

CMD_HELP.update(
    {
        "purge": f"""
『 **Purge** 』
  `{PREFIX}del` -> Hapus pesan tertentu.
  `{PREFIX}purge` -> Hapus pesan balas.
  `{PREFIX}purgeme` -> Hapus beberapa pesan mu.
  `{PREFIX}purgeall` -> Hapus semua pesan siapa aja, ijin admin.
"""
    }
)


@app.on_message(filters.command("purge", PREFIX) & filters.me)
async def purge_message(client, message):
    try:
        if message.reply_to_message:
            await message.edit("Menghapus pesan...")
            start = datetime.now()
            kontol = await app.get_messages(
            			message.chat.id,
            			range(message.reply_to_message.id, message.id),
            			replies=0
            		)
            msg_id = []
            msg_id.clear()
            for msg in kontol:
                 msg_id.append(msg.id)
            await app.delete_messages(
            			message.chat.id,
            			msg_id
            		)
            sec = (datetime.now() - start).seconds
            await message.edit(f"Deleted `{len(msg_id)}` messages in `{sec}` seconds.")
            await asyncio.sleep(5)
            await message.delete()
        else:
            await message.edit("Tolong balas ke pesan")
    except RPCError:
        await message.edit("Maaf anda bukan admin")
            
@app.on_message(filters.command("del", PREFIX) & filters.me)
async def delete_replied(client, message):
    msg_ids = [message.id]
    if message.reply_to_message:
        msg_ids.append(message.reply_to_message.id)
    await app.delete_messages(message.chat.id, msg_ids)
    
@app.on_message(filters.command("purgeme", PREFIX) & filters.me)
async def purge_me(client, message):
    if len(message.command) != 2:
        return
    n = message.text.split(None, 1)[1].strip()
    if not n.isnumeric():
        return await message.edit("Invalid jumlah pesan")
    n = int(n)
    if n < 1:
        return await message.edit("Silahkan kombinasi dengan angka")
    chat_id = message.chat.id
    message_ids = [
        m.id
        async for m in app.search_messages(
            chat_id,
            from_user="me",
            limit=n,
        )
    ]
    if not message_ids:
        return await message.edit("Pesan tidak di temukan")
    to_delete = [message_ids[i : i + 99] for i in range(0, len(message_ids), 99)]
    for hundred_messages_or_less in to_delete:
        await app.delete_messages(
            chat_id=chat_id,
            message_ids=hundred_messages_or_less,
            revoke=True,
        )
    ms_g = await app.send_message(
        message.chat.id,
        f"Berhasil menghapus {n} pesan kenangan",
    )
    await asyncio.sleep(5)
    await ms_g.delete()

@app.on_message(filters.command("purgeall", PREFIX) & filters.me)
async def purge_all(client, message):
    memek = message.reply_to_message
    if not memek:
        await message.edit("silahkan balas ke pesan orang atau diri sendiri untuk menghapus semua pesan sekaligus")
        return
    else:
        try:
            turok = memek.from_user.id
            bisa = await app.get_users(turok)
            await message.edit("Mulai menghapus semua pesan anda")
            await app.delete_user_history(message.chat.id, bisa.id)
        except RPCError:
            await message.edit("Maaf anda bukan Admin")
