# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
# yukki
# All rights reserved.

import asyncio
import math

import dotenv
import heroku3
import requests
from pyrogram import filters

from config import HEROKU_API, HEROKU_APP_NAME, PREFIX
from Prime import CMD_HELP, app
from Prime.helpers.heroku import is_heroku

CMD_HELP.update(
    {
        "heroku": f"""
『 **Heroku** 』
  `{PREFIX}usage` -> Cek dyno.
  `{PREFIX}dyno` -> Fake cek dyno.
  `{PREFIX}set_var` - > Ubah var heroku.
  `{PREFIX}del_var` -> Hapus var heroku.
  `{PREFIX}get_var` -> Cek var heroku.
"""
    }
)


@app.on_message(filters.command("get_var", PREFIX) & filters.me)
async def varget_(client, message):
    usage = f"**Usage:**\n{PREFIX}get_var [Var Name]"
    if len(message.command) != 2:
        return await message.edit_text(usage)
    check_var = message.text.split(None, 2)[1]
    if await is_heroku():
        if HEROKU_API == "" and HEROKU_APP_NAME == "":
            return await message.edit_text(
                "**HEROKU APP DETECTED!**\n\nUntuk memperbarui aplikasi, Anda perlu menyiapkan vars `HEROKU_API` dan `HEROKU_APP_NAME` vars masing-masing!"
            )
        elif HEROKU_API == "" or HEROKU_APP_NAME == "":
            return await message.edit_text(
                "**HEROKU APP DETECTED!**\n\n**Pastikan untuk menambahkan keduanya** `HEROKU_API` dan `HEROKU_APP_NAME` **vars dengan benar agar dapat memperbarui dari jarak jauh!**"
            )
        try:
            Heroku = heroku3.from_key(HEROKU_API)
            happ = Heroku.app(HEROKU_APP_NAME)
        except BaseException:
            return await message.edit_text(
                "Harap pastikan Heroku API Key anda, Nama Aplikasi Anda dikonfigurasi dengan benar di heroku"
            )
        heroku_config = happ.config()
        if check_var in heroku_config:
            return await message.edit_text(
                f"**Heroku Config:\n\n{check_var}: `{heroku_config[check_var]}`**"
            )
        else:
            return await message.edit_text("Tidak ada Var seperti itu")
    else:
        path = dotenv.find_dotenv()
        if not path:
            return await message.edit_text(".env tidak di temukan")
        output = dotenv.get_key(path, check_var)
        if not output:
            return await message.edit_text("Tidak ada Var seperti itu")
        else:
            return await message.edit_text(f".env:\n\n**{check_var}:** `{str(output)}`")


@app.on_message(filters.command("del_var", PREFIX) & filters.me)
async def vardel_(client, message):
    usage = f"**Usage:**\n{PREFIX}del_var [Var Name]"
    if len(message.command) != 2:
        return await message.edit_text(usage)
    check_var = message.text.split(None, 2)[1]
    if await is_heroku():
        if HEROKU_API == "" and HEROKU_APP_NAME == "":
            return await message.edit_text(
                "**HEROKU APP DETECTED!**\n\nUntuk memperbarui aplikasi, Anda perlu menyiapkan vars `HEROKU_API` dan `HEROKU_APP_NAME` vars masing-masing!"
            )
        elif HEROKU_API == "" or HEROKU_APP_NAME == "":
            return await message.edit_text(
                "**HEROKU APP DETECTED!**\n\n**Pastikan untuk menambahkan keduanya** `HEROKU_API` dan `HEROKU_APP_NAME` **vars dengan benar agar dapat memperbarui dari jarak jauh!**"
            )
        try:
            Heroku = heroku3.from_key(HEROKU_API)
            happ = Heroku.app(HEROKU_APP_NAME)
        except BaseException:
            return await message.edit_text(
                "Harap pastikan Heroku API Key anda, Nama Aplikasi Anda dikonfigurasi dengan benar di heroku"
            )
        heroku_config = happ.config()
        if check_var in heroku_config:
            await message.edit_text(
                f"**Hapus Heroku Var :**\n\n`{check_var}`.Berhasil di hapus."
            )
            del heroku_config[check_var]
        else:
            return await message.edit_text(f"Tidak ada Var seperti itu")
    else:
        path = dotenv.find_dotenv()
        if not path:
            return await message.edit_text(".env Tidak di temukan.")
        output = dotenv.unset_key(path, check_var)
        if not output[0]:
            return await message.edit_text("Tidak ada var seperti itu")
        else:
            return await message.edit_text(
                f".env Var Deletion:\n\n`{check_var}` telah berhasil dihapus. Untuk memulai ulang perintah bot ketik {PREFIX}restart."
            )
            os.system(f"kill -9 {os.getpid()} && python3 -m Prime")



@app.on_message(filters.command("set_var", PREFIX) & filters.me)
async def set_var(client, message):
    usage = f"**Usage:**\n{PREFIX}set_var [Var Name] [Var Value]"
    if len(message.command) < 3:
        return await message.edit_text(usage)
    to_set = message.text.split(None, 2)[1].strip()
    value = message.text.split(None, 2)[2].strip()
    if await is_heroku():
        if HEROKU_API == "" and HEROKU_APP_NAME == "":
            return await message.edit_text(
                "**HEROKU APP DETECTED!**\n\nUntuk memperbarui aplikasi, Anda perlu menyiapkan vars `HEROKU_API` dan `HEROKU_APP_NAME` vars masing-masing!"
            )
        elif HEROKU_API == "" or HEROKU_APP_NAME == "":
            return await message.edit_text(
                "**HEROKU APP DETECTED!**\n\n**Pastikan untuk menambahkan keduanya** `HEROKU_API` dan `HEROKU_APP_NAME` **vars dengan benar agar dapat memperbarui dari jarak jauh!**"
            )
        try:
            Heroku = heroku3.from_key(HEROKU_API)
            happ = Heroku.app(HEROKU_APP_NAME)
        except BaseException:
            return await message.edit_text(
                "Harap pastikan Heroku API Key anda, Nama Aplikasi Anda dikonfigurasi dengan benar di heroku"
            )
        heroku_config = happ.config()
        if to_set in heroku_config:
            await message.edit_text(
                f"**Heroku Var Updation:**\n\n`{to_set}` Telah berhasil di update. userbot akan memulai ulang."
            )
        else:
            await message.edit_text(
                f"Menambahkan var baru nama `{to_set}`. Userbot akan memulai ulang."
            )
        heroku_config[to_set] = value
    else:
        path = dotenv.find_dotenv()
        if not path:
            return await message.edit_text(".env Tidak di temukan.")
        dotenv.set_key(path, to_set, value)
        if dotenv.get_key(path, to_set):
            return await message.edit_text(
                f"**.env Var Updation:**\n\n`{to_set}` Berhasil di update. ketik {PREFIX}restart untuk memulai ulang userbot."
            )
        else:
            return await message.edit_text(
                f"**.env Ditambahkan :**\n\n`{to_set}` Berhasil di update. ketik {PREFIX}restart untuk memulai ulang userbot."
            )
            os.system(f"kill -9 {os.getpid()} && python3 -m Prime")


@app.on_message(filters.command("usage", PREFIX) & filters.me)
async def usage_dynos(client, message):
    ### Credits CatUserbot
    if await is_heroku():
        if HEROKU_API == "" and HEROKU_APP_NAME == "":
            return await message.edit_text(
                "**HEROKU APP DETECTED!**\n\nUntuk memperbarui aplikasi, Anda perlu menyiapkan vars `HEROKU_API` dan `HEROKU_APP_NAME` vars masing-masing!"
            )
        elif HEROKU_API == "" or HEROKU_APP_NAME == "":
            return await message.edit_text(
                "**HEROKU APP DETECTED!**\n\n**Pastikan untuk menambahkan keduanya** `HEROKU_API` dan `HEROKU_APP_NAME` **vars dengan benar agar dapat memperbarui dari jarak jauh!**"
            )
    else:
        return await message.edit_text("Hanya untuk Heroku Apps")
    try:
        Heroku = heroku3.from_key(HEROKU_API)
        Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await message.edit_text(
                "Harap pastikan Heroku API Key anda, Nama Aplikasi Anda dikonfigurasi dengan benar di heroku"
        )
    dyno = await message.edit_text("Check dyno heroku tolong tunggu")
    account_id = Heroku.account().id
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {HEROKU_API}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + account_id + "/actions/get-quota"
    r = requests.get("https://api.heroku.com" + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit("Unable to fetch.")
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    day = math.floor(hours / 24)
    await asyncio.sleep(1.5)
    text = f"""
╭┈─╼━━━━━━━━━━━━━╾─┈
│          ⚡PRIME USERBOT⚡  
├┈─╼━━━━━━━━━━━━━╾─┈ 
│✨ ᴘᴇɴɢɢᴜɴᴀᴀɴ ᴅʏɴᴏ ꜱᴀᴀᴛ ɪɴɪ
│  ▸ {AppHours} ᴊᴀᴍ - {AppMinutes} ᴍᴇɴɪᴛ.
│  ▸ ᴘʀᴇꜱᴇɴᴛᴀꜱᴇ : {AppPercentage}%
├┈──────────────┈
│✨ sɪsᴀ ᴅʏɴᴏ ʙᴜʟᴀɴ ɪɴɪ​
│  ▸ {hours} ᴊᴀᴍ - {minutes} ᴍᴇɴɪᴛ.
│  ▸ ᴘʀᴇꜱᴇɴᴛᴀꜱᴇ : {percentage}%.
╰┈─────────────┈ 
  ᴅʏɴᴏ ʜᴇʀᴏᴋᴜ : {day} ʜᴀʀɪ ʟᴀɢɪ​"""
    return await dyno.edit(text)



@app.on_message(filters.command("dyno", PREFIX) & filters.me)
async def fake_dynos(client, message):
    ### Credits CatUserbot
    if await is_heroku():
        if HEROKU_API == "" and HEROKU_APP_NAME == "":
            return await message.edit_text(
                "**HEROKU APP DETECTED!**\n\nUntuk memperbarui aplikasi, Anda perlu menyiapkan vars `HEROKU_API` dan `HEROKU_APP_NAME` vars masing-masing!"
            )
        elif HEROKU_API == "" or HEROKU_APP_NAME == "":
            return await message.edit_text(
                "**HEROKU APP DETECTED!**\n\n**Pastikan untuk menambahkan keduanya** `HEROKU_API` dan `HEROKU_APP_NAME` **vars dengan benar agar dapat memperbarui dari jarak jauh!**"
            )
    else:
        return await message.edit_text("Hanya untuk Heroku Apps")
    try:
        Heroku = heroku3.from_key(HEROKU_API)
        Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await message.edit_text(
                "Harap pastikan Heroku API Key anda, Nama Aplikasi Anda dikonfigurasi dengan benar di heroku"
        )
    dyno = await message.edit_text("Check dyno heroku tolong tunggu")
    account_id = Heroku.account().id
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {HEROKU_API}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + account_id + "/actions/get-quota"
    r = requests.get("https://api.heroku.com" + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit("Unable to fetch.")
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    day = math.floor(hours / 24)
    FAppHours = math.floor(AppHours * 2)
    FAppMinutes = math.floor(AppMinutes * 2)
    Fhours = math.floor(hours * 2)
    Fminutes = math.floor(minutes * 2)
    Fday = math.floor(day * 2)
    await asyncio.sleep(1.5)
    text = f"""
╭┈─╼━━━━━━━━━━━━━╾─┈
│          ⚡PRIME USERBOT⚡  
├┈─╼━━━━━━━━━━━━━╾─┈ 
│✨ ᴘᴇɴɢɢᴜɴᴀᴀɴ ᴅʏɴᴏ ꜱᴀᴀᴛ ɪɴɪ
│  ▸ {FAppHours} ᴊᴀᴍ - {FAppMinutes} ᴍᴇɴɪᴛ.
│  ▸ ᴘʀᴇꜱᴇɴᴛᴀꜱᴇ : {AppPercentage}%
├┈──────────────┈
│✨ sɪsᴀ ᴅʏɴᴏ ʙᴜʟᴀɴ ɪɴɪ​
│  ▸ {Fhours} ᴊᴀᴍ - {Fminutes} ᴍᴇɴɪᴛ.
│  ▸ ᴘʀᴇꜱᴇɴᴛᴀꜱᴇ : {percentage}%.
╰┈─────────────┈ 
  ᴅʏɴᴏ ʜᴇʀᴏᴋᴜ : {Fday} ʜᴀʀɪ ʟᴀɢɪ​"""
    return await dyno.edit(text)
