# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

from . import cli

collection = cli["Prime"]["logs"]

# pmlogs
async def is_pmlogs(on_off: int) -> bool:
    onoff = await collection.find_one({"on_off": on_off})
    if not onoff:
        return False
    return True


async def add_on(on_off: int):
    is_on = await is_pmlogs(on_off)
    if is_on:
        return
    return await collection.insert_one({"on_off": on_off})


async def add_off(on_off: int):
    is_off = await is_pmlogs(on_off)
    if not is_off:
        return
    return await collection.delete_one({"on_off": on_off})
 
 
 # group   
async def is_gruplogs(off_on: int) -> bool:
    onoff = await collection.find_one({"off_on": off_on})
    if not onoff:
        return False
    return True


async def addg_on(off_on: int):
    is_on = await is_gruplogs(off_on)
    if is_on:
        return
    return await collection.insert_one({"off_on": off_on})


async def addg_off(off_on: int):
    is_off = await is_gruplogs(off_on)
    if not is_off:
        return
    return await collection.delete_one({"off_on": off_on})
