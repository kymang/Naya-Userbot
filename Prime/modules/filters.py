# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.


import re

from pyrogram import filters
from Prime import app, CMD_HELP
from config import PREFIX, LOG_CHAT
from Prime.helpers.pyrohelper import get_arg
from Prime.database.filtersdb import (
    add_filters,
    all_filters,
    del_filters,
    filters_del,
    filters_info,
)

CMD_HELP.update(
    {
        "filter": f"""
『 **Filters** 』
  `{PREFIX}filters` -> Daftar semua filter aktif dalam obrolan saat ini.
  `{PREFIX}filter [keyword]` -> Menyimpan filter.
  `{PREFIX}stop [keyword]` -> Menghentikan filter tertentu.
  `{PREFIX}stopall` -> Menghapus semua filter.
"""
    }
)


@app.on_message(filters.command("stop", PREFIX) & filters.me)
async def del_filterz(client, message):
    note_ = await message.edit("**Processing..**")
    note_name = get_arg(message)
    if not note_name:
        await note_.edit("**Jembut pake nama filter lah jancok**")
        return
    note_name = note_name.lower()
    if not await filters_info(note_name, int(message.chat.id)):
        await note_.edit("**Filter tidak ada!**")
        return
    await del_filters(note_name, int(message.chat.id))
    await note_.edit(f"**Filter `{note_name}` Sukses di hapus!**")


@app.on_message(filters.command("filters", PREFIX) & filters.me)
async def show_filters(client, message):
    pablo = await message.edit("**Processing..**")
    poppy = await all_filters(int(message.chat.id))
    if poppy is False:
        await pablo.edit("**Tidak ada filter di Chat ini...**")
        return
    kk = ""
    for Escobar in poppy:
        kk += f"\n ◍ `{Escobar.get('keyword')}`"
    X = await client.get_chat(int(message.chat.id))
    grp_nme = X.title
    mag = f"Daftar filter di {grp_nme}: \n{kk}"
    await pablo.edit(mag)


@app.on_message(filters.command("filter", PREFIX) & filters.me)
async def s_filters(client, message):
    note_ = await message.edit("**Processing..**")
    note_name = get_arg(message)
    if not note_name:
        await note_.edit("**Jembut pake nama filter lah jancok***")
        return
    if not message.reply_to_message:
        await note_.edit("**Bales ke pesan bego biar bisa pake filter")
        return
    note_name = note_name.lower()
    msg = message.reply_to_message
    copied_msg = await msg.copy(int(LOG_CHAT))
    await add_filters(note_name, int(message.chat.id), copied_msg.id)
    await note_.edit(f"**Done! `{note_name}` Sudah Masuk Filter masheh!**")


@app.on_message(
    filters.incoming & filters.group & ~filters.private & ~filters.me,
    group=3,
)
async def filter_s(client, message):
    owo = message.text
    al_fill = []
    is_m = False
    if not owo:
        return
    al_fil = await all_filters(int(message.chat.id))
    if not al_fil:
        return
    for all_fil in al_fil:
        al_fill.append(all_fil.get("keyword"))
    owoo = owo.lower()
    for filter_s in al_fill:
        pattern = r"( |^|[^\w])" + re.escape(filter_s) + r"( |$|[^\w])"
        if re.search(pattern, owo, flags=re.IGNORECASE):
            f_info = await filters_info(filter_s, int(message.chat.id))
            m_s = await client.get_messages(int(LOG_CHAT), f_info["msg_id"])
            if await is_media(m_s):
                text_ = m_s.caption or ""
                is_m = True
            else:
                text_ = m_s.text or ""
            if text_ != "":
                mention = message.from_user.mention
                user_id = message.from_user.id
                user_name = message.from_user.username or "No Username"
                first_name = message.from_user.first_name
                last_name = message.from_user.last_name or "No Last Name"
                text_ = text_.format(
                    mention=mention,
                    user_id=user_id,
                    user_name=user_name,
                    first_name=first_name,
                    last_name=last_name,
                )
            if not is_m:
                await client.send_message(
                    message.chat.id, text_, reply_to_message_id=message.id
                )
            else:
                await m_s.copy(
                    chat_id=int(message.chat.id),
                    caption=text_,
                    reply_to_message_id=message.id,
                )


async def is_media(message):
    if not (
        message.photo
        or message.video
        or message.document
        or message.audio
        or message.sticker
        or message.animation
        or message.voice
        or message.video_note
    ):
        return False
    return True


@app.on_message(filters.command("stopall", PREFIX) & filters.me)
async def del_all_filters(client, message):
    pablo = await message.edit("**Processing..**")
    poppy = await all_filters(int(message.chat.id))
    if poppy is False:
        await pablo.edit("**Yuhu gak ada filter bego di Chat ini...**")
        return
    await filters_del(int(message.chat.id))
    await pablo.edit("**Yeah, Berhasil di hapus semua filter masheh!**")
