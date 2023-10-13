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

import Prime.database.notesdb as Prime
from config import LOG_CHAT, PREFIX
from Prime import CMD_HELP, app
from Prime.helpers.pyrohelper import get_arg

CMD_HELP.update(
    {
        "notes": f"""
『 **Notes** 』
  `{PREFIX}save` -> Simpan catatan baru.
  `{PREFIX}get` -> Mendapatkan catatan yang ditentukan.
  `{PREFIX}clear` -> Menghapus catatan, ditentukan oleh nama catatan.
  `{PREFIX}clearall` -> Menghapus semua catatan yang disimpan.
  `{PREFIX}notes` -> Daftar catatan yang disimpan.
"""
    }
)

LOG_CHAT = LOG_CHAT


@app.on_message(filters.command("save", PREFIX) & filters.me)
async def save(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**Anda harus memberi nama untuk sebuah catatan.**")
        return
    note_name = arg
    note = await Prime.get_note(note_name)
    if note:
        await message.edit(f"**Note `{note_name}` sudah ada**")
        return
    reply = message.reply_to_message
    if not reply:
        await message.edit("Balas pesan untuk menyimpan catatan")
        return
    copy = await app.copy_message(LOG_CHAT, message.chat.id, reply.id)
    await Prime.save_note(note_name, copy.id)
    await message.edit("**Catatan berhasil di simpan**")


@app.on_message(filters.command("get", PREFIX) & filters.me)
async def get(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("Get apa jancok?")
        return
    note_name = arg
    note = await Prime.get_note(note_name)
    if not note:
        await message.edit(f"**Note {note_name} Tidak ada**")
        return
    if message.reply_to_message:
        await app.copy_message(
            message.chat.id,
            LOG_CHAT,
            note,
            reply_to_message_id=message.reply_to_message_id,
        )
    else:
        await app.copy_message(message.chat.id, LOG_CHAT, note)
    await message.delete()


@app.on_message(filters.command("clear", PREFIX) & filters.me)
async def clear(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("Apa yang ingin Anda hapus?")
        return
    note_name = arg
    note = await Prime.get_note(note_name)
    if not note:
        await message.edit(f"**Gagal menghapus catatan `{note_name}`**")
        return
    await Prime.rm_note(note_name)
    await message.edit(f"**Berhasil menghapus catatan `{note_name}`**")


@app.on_message(filters.command("notes", PREFIX) & filters.me)
async def notes(client, message):
    msg = "**Catatan Tersimpan**\n\n"
    all_notes = await Prime.all_notes()
    if not all_notes:
        await message.edit("**Tidak ada catatan yang disimpan**")
        return
    for notes in all_notes:
        msg += f"◍ `{notes}`\n"
    await message.edit(msg)


@app.on_message(filters.command("clearall", PREFIX) & filters.me)
async def clearall(client, message):
    await Prime.rm_all()
    await message.edit("**Menghapus semua catatan yang disimpan**")
