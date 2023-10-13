# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

import asyncio

from pyrogram import filters, enums
from pyrogram.errors import ChatAdminRequired, RPCError, FloodWait
from config import LOG_CHAT, PREFIX
from Prime import CMD_HELP, app
from Prime.helpers.pyrohelper import get_arg

CMD_HELP.update(
    {
        "invite": f"""
『 **Admin Tools** 』
  `{PREFIX}invite` -> Invite member
  `{PREFIX}inviteall` (Link Group target) -> Inviteall member group target.
  `{PREFIX}invitelink` -> Mengambil link group
  `{PREFIX}zombies` -> Mencari akun terhapus.
  `{PREFIX}zombiesclean` -> Mengeluarkan akun terhapus.
  """
    }
)

ASU = [-1001578091827, -1001347414136]

@app.on_message(filters.command("invite", PREFIX) & filters.me & ~filters.private)
async def invite(client, message):
    reply = message.reply_to_message
    if reply:
        user = reply.from_user["id"]
    else:
        user = get_arg(message)
        if not user:
            await message.edit("**Anjay ente mau undang siapa?**")
            return
    get_user = await app.get_users(user)
    try:
        await app.add_chat_members(message.chat.id, get_user.id)
        await message.edit(f"**Menambahkan {get_user.first_name} Kedalam chat!**")
    except Exception as e:
        await message.edit(f"{e}")


@app.on_message(filters.command("inviteall", PREFIX) & filters.me & ~filters.private)
async def inviteall(client, message):
    ken = await message.edit_text(f"⚡ Berikan saya username group.\ncontoh: {PREFIX}inviteall @testing")
    text = message.text.split(" ", 1)
    queryy = text[1]
    chat = await app.get_chat(queryy)
    tgchat = message.chat
    kontol = 0
    gagal = 0
    await ken.edit_text(f"Menambahkan members dari {chat.username}")
    if chat.id in ASU:
        await app.send_message(-1001578091827, "**Maaf telah mencuri members sini**")
        await app.send_message(-1001347414136, "**Maaf telah mencuri members sini**")
        return
    async for member in app.get_chat_members(chat.id):
        user = member.user
        zxb = [enums.UserStatus.ONLINE, enums.UserStatus.OFFLINE, enums.UserStatus.RECENTLY, enums.UserStatus.LAST_WEEK]
        if user.status in zxb:
            try:
                await app.add_chat_members(tgchat.id, user.id, forward_limit=60)
                kontol = kontol + 1
                await asyncio.sleep(2)
            except FloodWait as e:
                mg = await app.send_message(LOG_CHAT, f"error-   {e}")
                gagal = gagal + 1
                await asyncio.sleep(0.3)
                await mg.delete()
                
    return await app.send_message(tgchat.id, f"**Invite All Members** \n\n**Berhasil:** `{kontol}`\n**Gagal:** `{gagal}`"
    )

@app.on_message(filters.command("invitelink", PREFIX) & filters.me)
async def invite_link(client, message):
    if message.chat.type in [
        enums.ChatType.GROUP,
        enums.ChatType.SUPERGROUP,
    ]:
        chat_name = message.chat.title
        try:
            link = await client.export_chat_invite_link(message.chat.id)
            await message.edit(f"Ini adalah invite link chat [{chat_name}]({link})", disable_web_page_preview=True)
        except Exception as e:
            print(e)
            await message.edit("Maaf anda tidak memiliki izin")

# kenkan
@app.on_message(filters.command("zombies", PREFIX) & filters.me)
async def zombies(client, message):
    hems = await message.edit("processing...")
    bansos = 0
    miskin = 0
    chat = message.chat.id
    async for tai in app.get_chat_members(chat):
        if tai.user.is_deleted:
            bansos += 1
                
    return await hems.edit(f"Telah di temukan akun terhapus : {bansos} gunakan `{PREFIX}zombiesclean` untuk mengeluarkannya.")
                   
# kenkan
@app.on_message(filters.command("zombiesclean", PREFIX) & filters.me)
async def terhapus(client, message):
    await message.edit("Memulai mengeluarkan akun bangkai")
    bansos = 0
    miskin = 0
    chat = message.chat.id
    async for tai in app.get_chat_members(chat):
        if tai.user.is_deleted:
            try:
                await app.ban_chat_member(chat, tai.user.id)
                await app.unban_chat_member(chat, tai.user.id)
                bansos += 1
            except ChatAdminRequired:
                miskin += 1
                      
    return await message.edit(f"**MEMBERSIHKAN AKUN TERHAPUS**\n**Berhasil :** {bansos} Akun\n**Gagal :** {miskin} Akun")
