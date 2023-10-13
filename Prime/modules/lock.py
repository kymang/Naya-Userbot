# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

from pyrogram import filters
from pyrogram.types import ChatPermissions
from pyrogram.errors import RPCError
from Prime.helpers.pyrohelper import get_arg
from Prime import app, CMD_HELP
from config import PREFIX

CMD_HELP.update(
    {
        "lock": f"""
『 **Locks** 』
`{PREFIX}lock` (all atau jenis lock) -> Untuk mengunci grup dari aktivitas member.
`{PREFIX}unlock` (all atau jenis lock) -> Untuk membuka kunci grup.
Jenis lock : `msg` | `stickers` | `polls` | `media` | `invite` | `pin` | `url` | `info` | `gifs` | `all`
"""
    }
)


incorrect_parameters = f"Incorrect parameters, ketik `{PREFIX}help lock` untuk bantuan."

data = {
    "msg": "can_send_messages",
    "stickers": "can_send_other_messages",
    "gifs": "can_send_other_messages",
    "media": "can_send_media_messages",
    "games": "can_send_other_messages",
    "inline": "can_send_other_messages",
    "url": "can_add_web_page_previews",
    "polls": "can_send_polls",
    "info": "can_change_info",
    "invite": "can_invite_users",
    "pin": "can_pin_messages",
}

async def current_chat_permissions(chat_id):
    perms = []
    perm = (await app.get_chat(chat_id)).permissions
    if perm.can_send_messages:
        perms.append("can_send_messages")
    if perm.can_send_other_messages:
        perms.append("can_send_other_messages")
    if perm.can_send_media_messages:
        perms.append("can_send_media_messages")
    if perm.can_add_web_page_previews:
        perms.append("can_add_web_page_previews")
    if perm.can_send_polls:
        perms.append("can_send_polls")
    if perm.can_invite_users:
        perms.append("can_invite_users")
    if perm.can_pin_messages:
        perms.append("can_pin_messages")
        
    return perms

async def tg_lock(message, permissions: list, perm: str, lock: bool
):
    if lock:
        if perm not in permissions:
            return await message.edit_text("Already locked.")
        permissions.remove(perm)
    else:
        if perm in permissions:
            return await message.edit_edit("Already Unlocked.")
        permissions.append(perm)
    permissions = {perm: True for perm in list(set(permissions))}
    
    try:
        await app.set_chat_permissions(
            message.chat.id, ChatPermissions
            (**permissions)
        )
    except RPCError:
        return await message.edit(
            "To unlock this, you have to unlock `messages` first."
        )
    except RPCError:
        return await message.edit("`I don't have permission to do that.`")
    await message.edit(("locked" if lock else "Unlocked"))
    
@app.on_message(filters.command(["lock", "unlock"], PREFIX) & filters.me)
async def lock_func(client, message):
    if len(message.command) != 2:
        return await message.edit(incorrect_parameters)
    chat_id = message.chat.id
    parameter = message.text.strip().split(None, 1)[1].lower()
    state = message.command[0].lower()
    if parameter not in data and parameter != "all":
        return await message.edit(incorrect_parameters)
    permissions = await current_chat_permissions(chat_id)
    if parameter in data:
        await tg_lock(
            message, 
            permissions, 
            data[parameter], 
            bool(state == "lock"),
        )
    elif parameter == "all" and state == "lock":
        try:
            await app.set_chat_permissions(chat_id, ChatPermissions())
            await message.edit(f"Locked everything in {message.chat.title}")
        except RPCError:
            return await message.edit("`I don't have permission to do that.`")
    elif parameter == "all" and state == "unlock":
        try:
            await app.set_chat_permissions(
                chat_id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_other_messages=True,
                    can_send_media_messages=True,
                    can_add_web_page_previews=True,
                    can_send_polls=True,
                    can_invite_users=True,
                    can_change_info=False,
                    can_pin_messages=False,
                ),
            )
        except RPCError:
            return await message.edit("`I don't have permission to do that.`")
        await message.edit(f"Unlocked everyting in {message.chat.title}")
       
@app.on_message(filters.command("locks", PREFIX) & filters.me)
async def locktypes(client, message):
    permissions = await current_chat_permissions(message.chat.id)
    
    if not permissions:
        return await message.edit("No Permissions.")
    perms = ""
    for i in permissions:
        perms += f" • __**{i}**__\n"
            
    await message.edit(perms)
