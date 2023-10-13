# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

from . import cli

collection = cli["Prime"]["pmpermit"]

PMPERMIT_MESSAGE = (
    "**ROOM CHAT || PRIME USERBOT**\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "__HALLO SELAMAT DATANG, SAYA ADALAH BOT YANG MENJAGA ROOM CHAT INI MOHON JANGAN MELAKUKAN SPAM KARNA SAYA OTOMATIS AKAN MEMBLOKIR ANDA, TUNGGU SAMPAI TUAN MENERIMA PESAN ANDA__\n"
    "┏━━━━━━━━━━━━━━━━━━━\n"
    "┣[• PESAN OTOMATIS\n"
    "┣[• BY PRIME USERBOT\n"
    "┗━━━━━━━━━━━━━━━━━━━"
)

BLOCKED = (
    "**Anda Telah Di Blokir Karna Melakukan Spam Pesan\nKe Room Chat Prime Userbot ツ**"
)

LIMIT = 10

async def set_pm(value: bool):
    doc = {"_id": 1, "pmpermit": value}
    doc2 = {"_id": "Approved", "users": []}
    r = await collection.find_one({"_id": 1})
    r2 = await collection.find_one({"_id": "Approved"})
    if r:
        await collection.update_one({"_id": 1}, {"$set": {"pmpermit": value}})
    else:
        await collection.insert_one(doc)
    if not r2:
        await collection.insert_one(doc2)


async def set_permit_message(text):
    await collection.update_one({"_id": 1}, {"$set": {"pmpermit_message": text}})
    
async def set_block_message(text):
    await collection.update_one({"_id": 1}, {"$set": {"block_message": text}})


async def set_limit(limit):
    await collection.update_one({"_id": 1}, {"$set": {"limit": limit}})


async def get_pm_settings():
    result = await collection.find_one({"_id": 1})
    if not result:
        return False
    pmpermit = result["pmpermit"]
    pm_message = result.get("pmpermit_message", PMPERMIT_MESSAGE)
    block_message = result.get("block_message", BLOCKED)
    limit = result.get("limit", LIMIT)
    return pmpermit, pm_message, limit, block_message


async def allow_user(chat):
    doc = {"_id": "Approved", "users": [chat]}
    r = await collection.find_one({"_id": "Approved"})
    if r:
        await collection.update_one({"_id": "Approved"}, {"$push": {"users": chat}})
    else:
        await collection.insert_one(doc)


async def get_approved_users():
    results = await collection.find_one({"_id": "Approved"})
    if results:
        return results["users"]
    else:
        return []


async def deny_user(chat):
    await collection.update_one({"_id": "Approved"}, {"$pull": {"users": chat}})


async def pm_guard():
    result = await collection.find_one({"_id": 1})
    if not result:
        return False
    if not result["pmpermit"]:
        return False
    else:
        return True
