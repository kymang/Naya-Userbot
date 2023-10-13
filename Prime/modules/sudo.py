# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.
import heroku3
import asyncio
import os
from os import getenv
from pyrogram import filters
from config import PREFIX, HEROKU_APP_NAME, HEROKU_API
from Prime import CMD_HELP, app


CMD_HELP.update(
    {
        "sudo": f"""
『 **Sudo** 』
  `{PREFIX}addsudo` -> Menambahkan sudo user.
  `{PREFIX}delsudo` -> Menghapus sudo user.
  `{PREFIX}sudolist` -> Untuk melihat daftar sudo.
"""
    }
)

SUDO = {int(x) for x in os.getenv("SUDO", "").split()}

Heroku = heroku3.from_key(HEROKU_API)
heroku_api = "https://api.heroku.com"
sudoers = getenv("SUDO")



@app.on_message(filters.command("addsudo", PREFIX) & filters.me)
async def addsudo(client, message):
    jmbt = await message.edit("Sedang memproses...")
    vars = "SUDO"
    user = message.edit_to_message.from_user.id
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        await jmbt.edit(
            "**Silahkan Isi Var** `HEROKU_APP_NAME` **Untuk Menambahkan SUDO**",
        )
        return
    heroku_Config = app.config()
    if message is None:
       return
    users = f"{SUDO} {user}"
    sudo_user = (
        users.replace("{", "")
        .replace("}", "")
        .replace(",", "")
        .replace("[", "")
        .replace("]", "")
        .replace("set() ", "")
    )
    await jmbt.edit(
        f"**Berhasil Menambahkan** `{user}` **ke daftar SUDO.**\n\nSedang MeRestart Heroku untuk menerapkan perubahan."
    )
    heroku_Config[vars] = sudo_user

@app.on_message(filters.command("sudolist", PREFIX) & filters.me)
async def sudolist(client, message):
    users = "True" if SUDO else "False"
    sudo = sudoers
    list = sudo.replace(" ", "\n> ")
    if users == "True":
        await message.edit(
            f"**SUDO USER:** `Enable`\n\n**Sudo User:**\n> {list}\n\nKetik `{PREFIX}addsudo` di user yang ingin di tambahkan ke daftar sudo.",
        )
    else:
        await message.edit("**SUDO USER:** `Disable`")

@app.on_message(filters.command("delsudo", PREFIX) & filters.me)
async def delsudo(client, message):
    jmbt = await message.edit("`Sedang Memproses...`")
    user = message.edit_to_message.from_user.id
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        await jmbt.edit(
            "**Silahkan Tambahkan Vars** `HEROKU_APP_NAME` **Untuk menghapus sudo user**",
        )
        return
    heroku_Config = app.config()
    if message is None:
        return
    gett = str(user)
    if gett in sudoers:
        sudo_user = sudoers.replace(gett, "")
        await jmbt.edit(
            f"**Berhasil Menghapus** `{user}` **dari daftar Sudo.**\n\nSedang Merestart Heroku untuk menerapkan perubahan."
        )
        vars = "SUDO"
        heroku_Config[vars] = sudo_user
    else:
        await jmbt.edit(
            "**User ini tidak ada dalam daftar Sudo.**"
        )
