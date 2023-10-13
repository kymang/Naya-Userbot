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
from pyrogram.types import ChatPermissions, Message, ChatPrivileges
from pyrogram.errors import RPCError
from config import PREFIX
from Prime import CMD_HELP, app
from Prime.helpers.adminhelpers import CheckAdmin
from Prime.helpers.pyrohelper import get_arg, get_args

CMD_HELP.update(
    {
        "admin": f"""
『 **Admin Tools** 』
  `{PREFIX}ban` -> Blokir pengguna tanpa batas waktu.
  `{PREFIX}unban` -> Batalkan pemblokiran pengguna.
  `{PREFIX}promote` [optional title] -> Mempromosikan user.
  `{PREFIX}demote` _> Menurunkan user.
  `{PREFIX}mute` -> Membatasi user tanpa batas.
  `{PREFIX}unmute` -> Membatalkan mute user.
  `{PREFIX}kick` -> Mengeluarkan user dari group.
  `{PREFIX}kickme` -> Keluar sendiri dari group.
  `{PREFIX}gmute` -> Membatasi user secara global.
  `{PREFIX}ungmute` -> Membatalkan batasan user global.
  `{PREFIX}pin` -> pins pesan tertentu.
  `{PREFIX}unpin` -> Melepas pin pesan.
  `{PREFIX}unpinall` -> Melepas semua pin pesan grup.
"""
    }
)

unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True, 
    can_send_other_messages=True,
    can_send_polls=True,
    can_add_web_page_previews=True,
    can_change_info=False,
    can_pin_messages=False,
    can_invite_users=True,
)

mute_permission = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False, 
    can_send_other_messages=False,
    can_send_polls=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_pin_messages=False,
    can_invite_users=True,
)


@app.on_message(filters.command("ban", PREFIX) & filters.me)
async def ban_hammer(_, message: Message):
    if await CheckAdmin(message) is True:
        reply = message.reply_to_message
        if reply:
            user = reply.from_user.id
        else:
            user = get_arg(message)
            if not user:
                await message.edit("`Lah?? Gw bukan admin anjir disini!`")
                return
        try:
            get_user = await app.get_users(user)
            await app.ban_chat_member(
                chat_id=message.chat.id,
                user_id=get_user.id,
            )
            await message.edit(f"**Banned {get_user.first_name} Dari chat.**")
        except:
            await message.edit("`Lah?? Gw bukan Admin anjir disini!`")
    else:
        await message.edit("`Lah?? Gw bukan Admin anjir disini!`")


@app.on_message(filters.command("unban", PREFIX) & filters.me)
async def unban(_, message: Message):
    if await CheckAdmin(message) is True:
        reply = message.reply_to_message
        if reply:
            user = reply.from_user.id
        else:
            user = get_arg(message)
            if not user:
                await message.edit("`Lu mau unban siapa tolo?`")
                return
        try:
            get_user = await app.get_users(user)
            await app.unban_chat_member(chat_id=message.chat.id, user_id=get_user.id)
            await message.edit(f"**Unbanned {get_user.first_name} dari chat.**")
        except:
            await message.edit("`Gatau, Gakbisa di unban orangnya.`")
    else:
        await message.edit("`Lah?? Gw bukan Admin anjir disini!`")


# Mute Permissions


@app.on_message(filters.command("mute", PREFIX) & filters.me)
async def mute_hammer(_, message: Message):
    if await CheckAdmin(message) is True:
        reply = message.reply_to_message
        if reply:
            user = reply.from_user.id
        else:
            user = get_arg(message)
            if not user:
                await message.edit("`Lah?? Gw kan bukan Admin disini.`")
                return
        try:
            get_user = await app.get_users(user)
            await app.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=get_user.id,
                permissions=mute_permission,
            )
            await message.edit(f"**{get_user.first_name} Berhasil di muttte.**")
        except:
            await message.edit("`Gatau, Gabisa di muttte orangnya.`")
    else:
        await message.edit("Lah?? Gw bukan Admin anjir disini!`")


# Unmute permissions


@app.on_message(filters.command("unmute", PREFIX) & filters.me)
async def unmute(_, message: Message):
    if await CheckAdmin(message) is True:
        reply = message.reply_to_message
        if reply:
            user = reply.from_user.id
        else:
            user = get_arg(message)
            if not user:
                await message.edit("`Jembut, Lu mau muttte siapa?`")
                return
        try:
            get_user = await app.get_users(user)
            await app.restrict_chat_member(chat_id=message.chat.id,
               user_id=get_user.id,
               permissions=unmute_permissions,
               )
            await message.edit(f"**{get_user.first_name} Berhasil di unmuttte.**")
        except:
            await message.edit("`Gatau, Gakbisa di unmuttte orangnya.`")
    else:
        await message.edit("`Lah?? Gw bukan Admin anjir disini!`")


@app.on_message(filters.command("kick", PREFIX) & filters.me)
async def kick_user(_, message: Message):
    if await CheckAdmin(message) is True:
        reply = message.reply_to_message
        if reply:
            user = reply.from_user.id
        else:
            user = get_arg(message)
            if not user:
                await message.edit("`Jembut, Lu mau kick saha??`")
                return
        try:
            get_user = await app.get_users(user)
            await app.ban_chat_member(
                chat_id=message.chat.id,
                user_id=get_user.id,
            )
            await app.unban_chat_member(
                chat_id=message.chat.id,
                user_id=get_user.id,
            )
            await message.edit(f"**Kicked {get_user.first_name} Telah di tendang dari grupchat.**")
        except:
            await message.edit("`Gatau, Gakbisa di kick orangnya.`")
    else:
        await message.edit("`Lah?? Gw bukan Admin anjir disini!`")
        
@app.on_message(filters.command("kickme", PREFIX) & filters.me)
async def leave_chat(_, message: Message):
    if message.chat.type != "private":
        await message.edit("__Dahlah mending gw keluar...__")
        await asyncio.sleep(3)
        await message.chat.leave()
    else:
        await message.edit("`Lu gaboleh keluar dari gruplu sendiri tolol.`")


@app.on_message(filters.command("pin", PREFIX) & filters.me)
async def pin_message(_, message: Message):
    chat = message.chat.id
    ayang = message.reply_to_message
    try:
        await app.pin_chat_message(chat, ayang.id)
        await message.edit("**Berhasil menyematkan pesan di chat ini**")
    except RPCError:
        await message.edit("**Sepertinya Anda bukan admin disini**")

@app.on_message(filters.command("unpin", PREFIX) & filters.me)
async def unpin_message(_, message: Message):
    chat = message.chat.id
    ayang = message.reply_to_message
    try:
        await app.unpin_chat_message(chat, ayang.id)
        await message.edit("**Berhasil menghapus pesan tersemat di chat ini**")
    except RPCError:
        await message.edit("**Sepertinya Anda bukan admin disini**")

@app.on_message(filters.command("unpinall", PREFIX) & filters.me)    
async def unpin_all_message(_, message: Message):
    chat = message.chat.id
    ayang = message.reply_to_message
    try:
        await app.unpin_all_chat_message(chat, ayang.id)
        await message.edit("**Berhasil menghapus semua pesan tersemat di chat ini**")
    except RPCError:
        await message.edit("**Sepertinya Anda bukan admin disini**")

@app.on_message(filters.command("promote", PREFIX) & filters.me)
async def promote(client, message: Message):
    if await CheckAdmin(message) is False:
        await message.edit("`Lah?? Gw bukan Admin anjir disini!`")
        return
    title = "Admin"
    reply = message.reply_to_message
    if reply:
        user = reply.from_user.id
        title = str(get_arg(message))
    else:
        args = get_args(message)
        if not args:
            await message.edit("`Jembut, lu mau promote siapa?`")
            return
        user = args[0]
        if len(args) > 1:
            title = " ".join(args[1:])
    get_user = await app.get_users(user)
    try:
        await app.promote_chat_member(message.chat.id, user, ChatPrivileges(
            can_pin_messages=True,
            can_change_info=True,
            can_delete_messages=True,
            can_invite_users=True,
        )
                                     )
        await message.edit(
            f"`{get_user.first_name} Cie jadi Admin ya {title} Anjayyy🥶🥶`"
        )
    except Exception as e:
        await message.edit(f"{e}")
    if title:
        try:
            await app.set_administrator_title(message.chat.id, user, title)
        except:
            pass


@app.on_message(filters.command("demote", PREFIX) & filters.me)
async def demote(client, message: Message):
    if await CheckAdmin(message) is False:
        await message.edit("`Lu bukan admin goblok!`")
        return
    reply = message.reply_to_message
    if reply:
        user = reply.from_user.id
    else:
        user = get_arg(message)
        if not user:
            await message.edit("`Lu mau demote siapa?`")
            return
    get_user = await app.get_users(user)
    try:
        await app.promote_chat_member(
            message.chat.id,
            user,
            is_anonymous=False,
            can_change_info=False,
            can_delete_messages=False,
            can_edit_messages=False,
            can_invite_users=False,
            can_promote_members=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_post_messages=False,
        )
        await message.edit(
            f"`{get_user.first_name} Utututu:(.... Ciiaann bukan ADMIN lagi.`"
        )
    except Exception as e:
        await message.edit(f"{e}")


@app.on_message(filters.command("kickall", PREFIX) & filters.me)
async def kickall(client, message):
    await message.edit("`Mengeluarkan semua member...`")
    member = app.get_chat_members(message.chat.id)
    async for alls in member:
        try:
            await app.ban_chat_member(message.chat.id, alls.user.id, 0)
        except:
            pass
