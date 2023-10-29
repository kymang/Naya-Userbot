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

BOT_TOKEN = os.environ.get("BOT_TOKEN", "6520515685:AAHrYg1X4Z5byOQqHW_y7a_BoOvFAJ4dJ1k")
API_ID = int(os.environ.get("API_ID", "28358285"))
API_HASH = os.environ.get("API_HASH", "8930157ab19270574cd27b89f215d49a")

Bot = Client("Server",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN)
            
print("Server Berhasil Diaktifkan")

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

        
@Bot.on_message(filters.private & filters.command("start"))
async def start_message(client, message):
    bot = await Bot.get_me()
    await Bot.send_message(
        message.chat.id,
        text=f"Halo {message.from_user.mention}",
        reply_markup=InlineKeyboardMarkup(
                [
                    [
                     InlineKeyboardButton("Deploy", callback_data="adubot")
                    ]
               ]
            )
    )
    

@Bot.on_callback_query(filters.regex("deploy"))
async def deployprime(client, callback_query):
    await callback_query.message.reply(
    text = "Pilih salah satu dibawah ini",
    reply_markup = InlineKeyboardMarkup(
                    [
                        [
                         InlineKeyboardButton("LOGIN", callback_data="adubot")
                        ],
                   ]
                )
    )
    
@Bot.on_callback_query(filters.regex("adubot"))
async def cbprimeubot(client, callback_query):
    await prime_userbot(client, callback_query.message)

@Bot.on_callback_query(filters.regex("session"))
async def cbsession(client, callback_query):
    await prime_userbot1(client, callback_query.message)
    

async def prime_userbot(client, message):
    user_id = message.chat.id
    repository_msg = await Bot.ask(user_id, "Masukkan repository GitHub kamu, cth: https://github.com/user/repo", filters=filters.text)
    if await is_cancel(repository_msg):
        return
    repository_url = repository_msg.text

    heroku_api = await Bot.ask(user_id, "Masukkan HEROKU_API jing...**\n\nAmbil Disini Pler (https://dashboard.heroku.com/account/applications/authorizations/new)", filters=filters.text)
    if await is_cancel(heroku_api):
        return
    api_heroku = heroku_api.text
    memek = heroku3.from_key(api_heroku)
    hasil_conn = test_connection(memek)
    if not hasil_conn:
        await Bot.send_message(user_id, "**HEROKU_API salah goblog** Ulangin dari awal!")
        return
    else:
        await Bot.send_message(user_id, "**lagi ngecek HEROKU_API_KEY**")
        
    api_id_msg = await Bot.ask(user_id, "**Masukin** `API_ID` jing...", filters=filters.text)
    if await is_cancel(heroku_api):
        return
    api_id = int(api_id_msg.text)
    api_hash_msg = await Bot.ask(user_id, "**Masukin** `API_HASH` jing...", filters=filters.text)
    if await is_cancel(heroku_api):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await Bot.ask(user_id, 'Masukin nomer telemu bangsat, Jangan nomer mamakmu. \nContoh : `+19876543210`', filters=filters.text)
    phone_number = phone_number_msg.text
    client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = await client.send_code(phone_number)
    except ApiIdInvalid:
        await message.reply('`API_ID` dan `API_HASH` Kombinasinya ga valid. Lu Tolol apa gimane?, ulangin dari awal geh jing...')
        return
    except PhoneNumberInvalid:
        await message.reply('`Nomer telemu` Tidak valid. Pasti yg kau masukin tadi nomer mamakmu.\n Ulangin jing...')
        return
    try:
        phone_code_msg = await Bot.ask(user_id, "Masukin Kodenya, make spasi ya pler\nContoh : 1 2 3 4 5", filters=filters.text, timeout=600)
    except TimeoutError:
        await message.reply('Ahh goblok, kelamaan ngantuk gua, ulangin kalo lu mau bikin lagi')
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except PhoneCodeInvalid:
        await message.reply('Kodenya Salah GOBLOK')
        return
    except PhoneCodeExpired:
        await message.reply('Kodenya Kadaluwarsa TOLOL...')
        return
    except SessionPasswordNeeded:
        try:
            two_step_msg = await Bot.ask(user_id, 'Aelah make dipassword lagi akun jelek, MASUKIN PASSWORD AKUN LU KESINI NGENTOT.', filters=filters.text, timeout=300)
        except TimeoutError:
            await message.reply('Ahh goblok, kelamaan ngantuk gua, ulangin kalo lu mau bikin lagi.')
            return
        try:
            password = two_step_msg.text
            await client.check_password(password=password)
        except PasswordHashInvalid:
            await two_step_msg.reply('Katasandimu salah Tolol, makanya gausa make password jing....', quote=True)
            return
    session = await client.export_session_string()
    text = f"**STRINGNYA DAH JADI NIH JING...** \n\n`{session}` \n\nMinimal bilang makasih dulu."
    await client.send_message("me", text)
    await client.disconnect()
    
    mongo_msg = await Bot.ask(user_id, "**Masukin** `MONGO_URI`\nAmbilnya dimana?, Usaha ngentot jangan nanya mulu anjing.", filters=filters.text)
    if await is_cancel(heroku_api):
        return
    name_ku = "nekasjd" + str(time() * 1000)[-4:].replace(".", "") + str(random.randint(0,500))
    memek.create_app(name=name_ku, stack_id_or_name="heroku-22", region_id_or_name="eu")
    
    mongo_uri = mongo_msg.text
    kontol = memek.app(name_ku)
    var_heroku = kontol.config()
    var_heroku["API_ID"] = api_id
    var_heroku["API_HASH"] = api_hash
    var_heroku["SESSION"] = session
    var_heroku["HEROKU_API"] = api_heroku
    var_heroku["HEROKU_APP_NAME"] = name_ku
    var_heroku["MONGO_URI"] = mongo_uri

    await Bot.send_message(user_id, "✅ **Lagi proses deploy, Tungguin ae sambil Coli...**")

    buildpack_urls = ['heroku/python', 'https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git']
    kontol.update_buildpacks(buildpack_urls)

    repo_msg = await Bot.ask(user_id, "Masukkan HEROKU_URL/Repository URL-nya", filters=filters.text)
    HEROKU_URL = repo_msg.text if repo_msg else None

    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(HEROKU_URL)
    else:
        remote = repo.create_remote("heroku", HEROKU_URL)

    try:
        remote.push(refspec="HEAD:refs/heads/master", force=True)
    except BaseException as error:
        return await message.reply(f"Error \nTraceBack : {error}")

    kontol.process_formation()

    await Bot.send_message(user_id, "✅ Done mas")
    

async def prime_userbot1(client, message):
    user_id = message.chat.id
    heroku_api = await Bot.ask(user_id, "**Silahkan masukkan HEROKU_API anda**\n\n[KLIK DI SINI](https://dashboard.heroku.com/account/applications/authorizations/new)", filters=filters.text)
    if await is_cancel(heroku_api):
        return
    api_heroku = heroku_api.text
    memek = heroku3.from_key(api_heroku)
    hasil_conn = test_connection(memek)
    if not hasil_conn:
        await Bot.send_message(user_id, "**HEROKU_API Salah silahkan klik** /start")
        return
    else:
        await Bot.send_message(user_id, "**HEROKU_API_KEY benar**")
    
    api_id_msg = await Bot.ask(user_id, "**Tolong masukkan** `API_ID`\nDapatkan di my.telegram.org.")
    if await is_cancel(heroku_api):
        return
    api_id = int(api_id_msg.text)
    api_hash_msg = await Bot.ask(user_id, "**Tolong masukkan** `API_HASH`\nDapatkan di my.telegram.org.")
    if await is_cancel(heroku_api):
        return
    api_hash = api_hash_msg.text
    session_msg = await Bot.ask(user_id, "**Tolong masukkan** `SESSION`\nGunakan bot string apa aja dan pilih Pyrogram v2")
    if await is_cancel(heroku_api):
        return
    mongo_msg = await Bot.ask(user_id, "**Tolong masukkan** `MONGO_URI`\nKamu bisa dapatkan di mongodb.com.")
    if await is_cancel(heroku_api):
        return
    name_ku = "ubot" + str(int(time.time() * 1000))[-4:].replace(".", "") + str(random.randint(0, 500))
    name_ku = "a" + name_ku + "z"  # Menambahkan "a" di awal dan "z" di akhir
    name_ku = name_ku.lower()  # Mengonversi ke huruf kecil jika ada huruf besar

# Pastikan hanya mengandung karakter yang diizinkan
    name_ku = ''.join(filter(lambda x: x.isalnum() or x == "-", name_ku))

# Selanjutnya, gunakan name_ku dalam pembuatan aplikasi
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

    await Bot.send_message(user_id, "✅ **Lagi proses deploy, Tungguin ae sambil Coli...**")

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
    
    kontol.process_formation()

    await Bot.send_message(user_id, "**✅ Nah dah berhasil nih mek**")
    
async def is_cancel(message):
    if "/cancel" in message.text:
        await message.reply("**Membatalkan proses pembuatan!**")
        return True
    elif message.text.startswith("/"):
        await message.reply("**Membatalkan proses pembuatan!**")
        return True
    else:
        return False


Bot.run()
idle()
