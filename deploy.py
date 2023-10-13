import os
import asyncio
import random
import shlex
import socket
from time import time
from typing import Tuple
import heroku3
import sys
from os import environ, execle, path, remove
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
import requests
from heroku3.core import test_connection
from heroku3.helpers import validate_name
from pyrogram import Client, filters, idle
from pyromod import listen
from git import Repo
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)

from dotenv import load_dotenv

load_dotenv("p.env")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "5430644718:AAF1ms28hsa9GvoaggywA7c8EuQm0uXKvBc")
API_ID = int(os.environ.get("API_ID", "5469720"))
API_HASH = os.environ.get("API_HASH", "d69086dbd5605db7bfdf334daff7b917")

Bukan = Client("BukanDev",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN)
            
print("Bot telah aktif")

async def updateme_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)

def fetch_heroku_git_url(api_heroku, name_ku):
    heroku = heroku3.from_key(api_heroku)
    try:
        heroku_applications = heroku.apps()
    except:
        return None
    heroku_app = None
    for app in heroku_applications:
        if app.name == name_ku:
            heroku_app = app
            break
    if not heroku_app:
        return None
    return heroku_app.git_url.replace("https://", "https://api:" + api_heroku + "@")

        
@Bukan.on_message(filters.private & filters.command("start"))
async def start_message(client, message):
    bot = await Bukan.get_me()
    await Bukan.send_message(
        message.chat.id,
        text=f"Hay {message.from_user.mention} saya adalah {bot.mention} Akan membantu kamu dalam mendeploy repo kami di heroku silahkan pilih repo mana aja yg mau di deploy.",
        reply_markup=InlineKeyboardMarkup(
                [
                    [
                     InlineKeyboardButton("PRIME-USERBOT", callback_data="deploy")
                    ]
               ]
            )
    )
    

@Bukan.on_callback_query(filters.regex("deploy"))
async def deployprime(client, callback_query):
    await callback_query.message.reply(
    text = "Silahkan pilih di bawah ini \n=> LOGIN -> deploy via nomer\n=> SESSION -> Deploy via strings",
    reply_markup = InlineKeyboardMarkup(
                    [
                        [
                         InlineKeyboardButton("LOGIN", callback_data="prime")
                        ],
                        [
                        InlineKeyboardButton("SESSION", callback_data="session")
                        ]
                   ]
                )
    )
    
@Bukan.on_callback_query(filters.regex("prime"))
async def cbprimeubot(client, callback_query):
    await prime_userbot(client, callback_query.message)

@Bukan.on_callback_query(filters.regex("session"))
async def cbsession(client, callback_query):
    await prime_userbot1(client, callback_query.message)
    

async def prime_userbot(client, message):
    user_id = message.chat.id
    heroku_api = await Bukan.ask(user_id, "**Silahkan masukkan HEROKU_API anda**\n\n[KLIK DI SINI](https://dashboard.heroku.com/account/applications/authorizations/new)", filters=filters.text)
    if await is_cancel(heroku_api):
        return
    api_heroku = heroku_api.text
    memek = heroku3.from_key(api_heroku)
    hasil_conn = test_connection(memek)
    if not hasil_conn:
        await Bukan.send_message(user_id, "**HEROKU_API Salah silahkan klik** /start")
        return
    else:
        await Bukan.send_message(user_id, "**HEROKU_API_KEY benar**")
        
    api_id_msg = await Bukan.ask(user_id, "**Tolong masukkan** `API_ID`\nDapatkan di my.telegram.org.", filters=filters.text)
    if await is_cancel(heroku_api):
        return
    api_id = int(api_id_msg.text)
    api_hash_msg = await Bukan.ask(user_id, "**Tolong masukkan** `API_HASH`\nDapatkan di my.telegram.org.", filters=filters.text)
    if await is_cancel(heroku_api):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await Bukan.ask(user_id, 'Sekarang kirimkan `PHONE_NUMBER` Anda beserta kode negaranya. \nContoh : `+19876543210`', filters=filters.text)
    phone_number = phone_number_msg.text
    client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = await client.send_code(phone_number)
    except ApiIdInvalid:
        await message.reply('`API_ID` dan `API_HASH` Kombinasi tidak valid. Silakan mulai membuat sesi lagi.')
        return
    except PhoneNumberInvalid:
        await message.reply('`PHONE_NUMBER` Tidak valid. Silakan mulai membuat sesi lagi')
        return
    try:
        phone_code_msg = await Bukan.ask(user_id, "Silakan periksa OTP di akun telegram resmi. Jika Anda mendapatkannya, Kirim OTP di sini setelah membaca format di bawah ini. \nJika kode OTP dalam bentuk ~ `12345`, **silakan kirim sebagai** `1 2 3 4 5`.", filters=filters.text, timeout=600)
    except TimeoutError:
        await message.reply('Batas waktu tercapai 10 menit. Silakan mulai membuat sesi lagi.')
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except PhoneCodeInvalid:
        await message.reply('OTP is invalid. Please start generating session again.')
        return
    except PhoneCodeExpired:
        await message.reply('Kode OTP Kadaluarsa. Silakan mulai membuat sesi lagi.')
        return
    except SessionPasswordNeeded:
        try:
            two_step_msg = await Bukan.ask(user_id, 'Akun Anda telah mengaktifkan verifikasi dua langkah. Harap berikan kata sandinya.', filters=filters.text, timeout=300)
        except TimeoutError:
            await message.reply('Batas waktu tercapai 5 menit. Silakan mulai membuat sesi lagi.')
            return
        try:
            password = two_step_msg.text
            await client.check_password(password=password)
        except PasswordHashInvalid:
            await two_step_msg.reply('Kata sandi salah. Silakan mulai membuat sesi lagi.', quote=True)
            return
    session = await client.export_session_string()
    text = f"**PYROGRAM V2 STRING SESSION** \n\n`{session}` \n\nGenerated by @PrimeSupportGroup"
    await client.send_message("me", text)
    await client.disconnect()
    
    mongo_msg = await Bukan.ask(user_id, "**Tolong masukkan** `MONGO_URI`\nKamu bisa dapatkan di mongodb.com.", filters=filters.text)
    if await is_cancel(heroku_api):
        return
    name_ku = "prime" + str(time() * 1000)[-4:].replace(".", "") + str(random.randint(0,500))
    memek.create_app(name=name_ku, region_id_or_name="eu")
    
    mongo_uri = mongo_msg.text
    kontol = memek.app(name_ku)
    var_heroku = kontol.config()
    var_heroku["API_ID"] = api_id
    var_heroku["API_HASH"] = api_hash
    var_heroku["SESSION"] = session
    var_heroku["HEROKU_API"] = api_heroku
    var_heroku["HEROKU_APP_NAME"] = name_ku
    var_heroku["MONGO_URI"] = mongo_uri

    await Bukan.send_message(user_id, "✅ **Proses deploy Prime Userbot, Harap tunggu.. Akan ada pesan dari saya jika sudah siap untuk di-deploy ... Menunggu 3-5 menit**")

    buildpack_urls = ['heroku/python', 'https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git'] 
    kontol.update_buildpacks(buildpack_urls)

    repo = Repo()
    HEROKU_URL = None
    if api_heroku and name_ku:
        HEROKU_URL = fetch_heroku_git_url(api_heroku, name_ku) 
        
    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(HEROKU_URL)
    else:
        remote = repo.create_remote("heroku",HEROKU_URL)
    try:
        remote.push(refspec="HEAD:refs/heads/master", force=True)
    except BaseException as error:
        return await message.reply(f"**Error** \nTraceBack : `{error}`")
    
    kontol.process_formation()["worker"].scale(1)

    await Bukan.send_message(user_id, "**✅ Prime Userbot Telah berhasil di deploy**")
    

async def prime_userbot1(client, message):
    user_id = message.chat.id
    heroku_api = await Bukan.ask(user_id, "**Silahkan masukkan HEROKU_API anda**\n\n[KLIK DI SINI](https://dashboard.heroku.com/account/applications/authorizations/new)", filters=filters.text)
    if await is_cancel(heroku_api):
        return
    api_heroku = heroku_api.text
    memek = heroku3.from_key(api_heroku)
    hasil_conn = test_connection(memek)
    if not hasil_conn:
        await Bukan.send_message(user_id, "**HEROKU_API Salah silahkan klik** /start")
        return
    else:
        await Bukan.send_message(user_id, "**HEROKU_API_KEY benar**")
    
    api_id_msg = await Bukan.ask(user_id, "**Tolong masukkan** `API_ID`\nDapatkan di my.telegram.org.")
    if await is_cancel(heroku_api):
        return
    api_id = int(api_id_msg.text)
    api_hash_msg = await Bukan.ask(user_id, "**Tolong masukkan** `API_HASH`\nDapatkan di my.telegram.org.")
    if await is_cancel(heroku_api):
        return
    api_hash = api_hash_msg.text
    session_msg = await Bukan.ask(user_id, "**Tolong masukkan** `SESSION`\nGunakan bot string apa aja dan pilih Pyrogram v2")
    if await is_cancel(heroku_api):
        return
    mongo_msg = await Bukan.ask(user_id, "**Tolong masukkan** `MONGO_URI`\nKamu bisa dapatkan di mongodb.com.")
    if await is_cancel(heroku_api):
        return
    name_ku = "prime" + str(time() * 1000)[-4:].replace(".", "") + str(random.randint(0,500))
    memek.create_app(name=name_ku, region_id_or_name="eu")
    
    
    mongo_uri = mongo_msg.text
    session = session_msg.text
    kontol = memek.app(name_ku)
    var_heroku = kontol.config()
    var_heroku["API_ID"] = api_id
    var_heroku["API_HASH"] = api_hash
    var_heroku["SESSION"] = session
    var_heroku["HEROKU_API"] = api_heroku
    var_heroku["HEROKU_APP_NAME"] = name_ku
    var_heroku["MONGO_URI"] = mongo_uri

    await Bukan.send_message(user_id, "✅ **Proses deploy Prime Userbot, Harap tunggu.. Akan ada pesan dari saya jika sudah siap untuk di-deploy ... Menunggu 3-5 menit**")

    buildpack_urls = ['heroku/python', 'https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git'] 
    kontol.update_buildpacks(buildpack_urls)

    repo = Repo()
    HEROKU_URL = None
    if api_heroku and name_ku:
        HEROKU_URL = fetch_heroku_git_url(api_heroku, name_ku) 
        
    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(HEROKU_URL)
    else:
        remote = repo.create_remote("heroku",HEROKU_URL)
    try:
        remote.push(refspec="HEAD:refs/heads/master", force=True)
    except BaseException as error:
        return await message.reply(f"**Error** \nTraceBack : `{error}`")
    
    kontol.process_formation()["worker"].scale(1)

    await Bukan.send_message(user_id, "**✅ Prime Userbot Telah berhasil di deploy**")
    
async def is_cancel(message):
    if "/cancel" in message.text:
        await message.reply("**Membatalkan proses pembuatan!**")
        return True
    elif message.text.startswith("/"):
        await message.reply("**Membatalkan proses pembuatan!**")
        return True
    else:
        return False


Bukan.run()
idle()
