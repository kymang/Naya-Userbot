# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.


import asyncio
import datetime
import math
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
from pyrogram.errors import StickersetInvalid, YouBlockedUser
from pyrogram.raw.functions.messages import GetStickerSet
from pyrogram.raw.types import InputStickerSetShortName
from pyrogram import filters, emoji
from typing import Tuple
from Prime.helpers.pyrohelper import get_arg
from pyrogram.types import Message
from Prime import app, CMD_HELP
from pyrogram.errors import RPCError

from config import PREFIX

CMD_HELP.update(
    {
        "sticker": f"""
『 **Sticker** 』
  `{PREFIX}kang` -> kangs stiker atau buat yang baru.
  `{PREFIX}stkrinfo` -> Dapatkan info paket stiker.
  `{PREFIX}tiny` -> Ubah sticker jadi kecil.
  `{PREFIX}mmf` [atas;bawah] -> Tambahkan tulisan di sticker.
  `{PREFIX}gets` -> Convert sricker jadi document.
  `{PREFIX}togif` -> Ubah sticker animasi video ke gif.
"""
    }
)


def get_text(message: Message) -> [None, str]:
    """Extract Text From Commands"""
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


async def run_cmd(cmd: str) -> Tuple[str, str, int, int]:
    """Run Commands"""
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


async def convert_to_image(message, client) -> [None, str]:
    """Convert Most Media Formats To Raw Image"""
    if not message:
        return None
    if not message.reply_to_message:
        return None
    final_path = None
    if not (
        message.reply_to_message.video
        or message.reply_to_message.photo
        or message.reply_to_message.sticker
        or message.reply_to_message.media
        or message.reply_to_message.animation
        or message.reply_to_message.audio
    ):
        return None
    if message.reply_to_message.photo:
        final_path = await message.reply_to_message.download()
    elif message.reply_to_message.sticker:
        if message.reply_to_message.sticker.mime_type == "image/webp":
            final_path = "webp_to_png_s_proton.png"
            path_s = await message.reply_to_message.download()
            im = Image.open(path_s)
            im.save(final_path, "PNG")
        else:
            path_s = await app.download_media(message.reply_to_message)
            final_path = "lottie_proton.png"
            cmd = (
                f"lottie_convert.py --frame 0 -if lottie -of png {path_s} {final_path}"
            )
            await run_cmd(cmd)
    elif message.reply_to_message.audio:
        thumb = message.reply_to_message.audio.thumbs[0].file_id
        final_path = await app.download_media(thumb)
    elif message.reply_to_message.video or message.reply_to_message.animation:
        final_path = "fetched_thumb.png"
        vid_path = await app.download_media(message.reply_to_message)
        await run_cmd(f"ffmpeg -i {vid_path} -filter:v scale=500:500 -an {final_path}")
    return final_path


@app.on_message(filters.command("stkrinfo", PREFIX) & filters.me)
async def packinfo(client, message):
    rep = await message.edit_text("`Processing...`")
    if not message.reply_to_message:
        await rep.edit("Tolong balas ke Sticker...")
        return
    if not message.reply_to_message.sticker:
        await rep.edit("Tolong balas ke Sticker...")
        return
    if not message.reply_to_message.sticker.set_name:
        await rep.edit("`Sepertinya Stiker Liar!.`")
        return
    stickerset = await app.send(
        GetStickerSet(
            stickerset=InputStickerSetShortName(
                short_name=message.reply_to_message.sticker.set_name
            ),
            hash=0,
        )
    )
    emojis = []
    for stucker in stickerset.packs:
        if stucker.emoticon not in emojis:
            emojis.append(stucker.emoticon)
    output = f"""**Sticker Pack Title **: `{stickerset.set.title}`
**Sticker Pack Short Name **: `{stickerset.set.short_name}`
**Stickers Count **: `{stickerset.set.count}`
**Archived **: `{stickerset.set.archived}`
**Official **: `{stickerset.set.official}`
**Masks **: `{stickerset.set.masks}`
**Animated **: `{stickerset.set.animated}`
**Emojis In Pack **: `{' '.join(emojis)}`
"""
    await rep.edit(output)


@app.on_message(filters.command("kang", PREFIX) & filters.me)
async def kang(client, message):
    rep = await message.edit_text("Menggunakan Megic Untuk Kang Stiker Ini...")
    if not message.reply_to_message:
        await rep.edit("Tolong Balas ke Stiker...")
        return
    Hell = get_text(message)
    name = ""
    pack = 1
    nm = message.from_user.username
    if nm:
        nam = message.from_user.username
        name = nam[1:]
    else:
        name = message.from_user.first_name
    packname = f"@{nm} Kang Pack {pack}"
    packshortname = f"Prime_{message.from_user.id}_{pack}"
    non = [None, "None"]
    emoji = "🤴"
    try:
        Hell = Hell.strip()
        if not Hell.isalpha():
            if not Hell.isnumeric():
                emoji = Hell
        else:
            emoji = "🤴"
    except:
        emoji = "🤴"
    exist = None
    is_anim = False
    if message.reply_to_message.sticker:
        if not Hell:
            emoji = message.reply_to_message.sticker.emoji or "😁"
        is_anim = message.reply_to_message.sticker.is_animated
        if is_anim:
            packshortname += "_animated"
            packname += " Animated"
        if message.reply_to_message.sticker.mime_type == "application/x-tgsticker":
            file_name = await message.reply_to_message.download("AnimatedSticker.tgs")
        else:
            cool = await convert_to_image(message, client)
            if not cool:
                await rep.edit("`Reply to a valid media first.`")
                return
            file_name = resize_image(cool)
    elif message.reply_to_message.document:
        if message.reply_to_message.document.mime_type == "application/x-tgsticker":
            is_anim = True
            packshortname += "_animated"
            packname += " Animated"
            file_name = await message.reply_to_message.download("AnimatedSticker.tgs")
    else:
        cool = await convert_to_image(message, client)
        if not cool:
            await rep.edit("`Reply to a valid media first.`")
            return
        file_name = resize_image(cool)
    try:
        exist = await app.send(
            GetStickerSet(
                stickerset=InputStickerSetShortName(short_name=packshortname), hash=0
            )
        )
    except StickersetInvalid:
        pass
    if exist:
        try:
            await app.send_message("stickers", "/addsticker")
        except YouBlockedUser:
            await rep.edit("`Please Unblock @Stickers`")
            await app.unblock_user("stickers")
        await app.send_message("stickers", packshortname)
        await asyncio.sleep(0.2)
        limit = "50" if is_anim else "120"
        while limit in await get_response(message):
            pack += 1
            prev_pack = int(pack) - 1
            await rep.edit(
                f"Kang Pack Vol __{prev_pack}__ is Full! Switching To Vol __{pack}__ Kang Pack"
            )
            packname = f"@{nm} Kang Pack {pack}"
            packshortname = f"Prime_{message.from_user.id}_{pack}"
            if is_anim:
                packshortname += "_animated"
                packname += " Animated"
            await app.send_message("stickers", packshortname)
            await asyncio.sleep(0.2)
            if await get_response(message) == "Invalid pack selected.":
                if is_anim:
                    await app.send_message("stickers", "/newanimated")
                else:
                    await app.send_message("stickers", "/newpack")
                await asyncio.sleep(0.5)
                await app.send_message("stickers", packname)
                await asyncio.sleep(0.2)
                await app.send_document("stickers", file_name)
                await asyncio.sleep(1)
                await app.send_message("stickers", emoji)
                await asyncio.sleep(0.5)
                await app.send_message("stickers", "/publish")
                if is_anim:
                    await app.send_message("stickers", f"<{packname}>")
                await app.send_message("stickers", "/skip")
                await asyncio.sleep(0.5)
                await app.send_message("stickers", packshortname)
                await rep.edit(
                    "**Sticker Kanged!** \n\n**Emoji:** {} \n**Pack:** [Here](https://t.me/addstickers/{})".format(
                        emoji, packshortname
                    )
                )
                return
        await app.send_document("stickers", file_name)
        await asyncio.sleep(1)
        await app.send_message("stickers", emoji)
        await asyncio.sleep(0.5)
        await app.send_message("stickers", "/done")
        await rep.edit(
            "**Sticker Kanged!** \n\n**Emoji:** {} \n**Pack:** [Here](https://t.me/addstickers/{})".format(
                emoji, packshortname
            )
        )
    else:
        if is_anim:
            await app.send_message("stickers", "/newanimated")
        else:
            await app.send_message("stickers", "/newpack")
        await app.send_message("stickers", packname)
        await asyncio.sleep(0.2)
        await app.send_document("stickers", file_name)
        await asyncio.sleep(1)
        await app.send_message("stickers", emoji)
        await asyncio.sleep(0.5)
        await app.send_message("stickers", "/publish")
        await asyncio.sleep(0.5)
        if is_anim:
            await app.send_message("stickers", f"<{packname}>")
        await app.send_message("stickers", "/skip")
        await asyncio.sleep(0.5)
        await app.send_message("stickers", packshortname)
        await rep.edit(
            "**Sticker Kanged!** \n\n**Emoji:** {} \n**Pack:** [Here](https://t.me/addstickers/{})".format(
                emoji, packshortname
            )
        )
        try:
            if os.path.exists(file_name):
                os.remove(file_name)
            downname = "./Downloads"
            if os.path.isdir(downname):
                shutil.rmtree(downname)
        except:
            print("Can't remove downloaded sticker files")
            return


async def get_response(message):
    return [x async for x in app.get_chat_history("Stickers", limit=1)][0].text

def resize_image(image):
    im = Image.open(image)
    maxsize = (512, 512)
    if (im.width and im.height) < 512:
        size1 = im.width
        size2 = im.height
        if im.width > im.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        im = im.resize(sizenew)
    else:
        im.thumbnail(maxsize)
    file_name = "Sticker.png"
    im.save(file_name, "PNG")
    if os.path.exists(image):
        os.remove(image)
    return file_name

@app.on_message(filters.command("gets", PREFIX) & filters.me)
async def getsticker(client, message):
    replied = message.reply_to_message
    chat = message.chat.id
    if not replied or not replied.sticker:
        return await edit_delete(event, "**Harap balas ke stiker**")
    xx = await message.edit("Mengconvert ke foto...")
    cool = await convert_to_image(message, client)
    file_name = resize_image(cool)
    await app.send_photo(chat, file_name, reply_to_message_id=message.reply_to_message.id)
    await xx.delete()


@app.on_message(filters.command("tiny", PREFIX) & filters.me)
async def tinysticker(client, message):
    r=message.reply_to_message
    if r:
        try:
            await message.edit("Yo merubah sticker jadi kecil")
            oh=await r.forward("@PrimeMegaBot")
            kon=await oh.reply("/tiny")
            await asyncio.sleep(4)
        except YouBlockedUser:
            await app.unblock_user("@PrimeMegaBot")
            await message.edit("Yo merubah sticker jadi kecil")
            await app.send_message("@PrimeMegaBot", "/start")
            oh=await r.forward("@PrimeMegaBot")
            kon=await oh.reply("/tiny")
            await asyncio.sleep(4)
        async for tiny in app.search_messages("@PrimeMegaBot", limit=1):
            if tiny:
                await message.delete()
                await message.reply_sticker(sticker=tiny.sticker.file_id, reply_to_message_id=message.reply_to_message.id)
            else:
                await message.edit("Sepertinya ada yang salah")
                
            await oh.delete()
            await kon.delete()
            await tiny.delete()

    else:
        return await message.edit("Silahkan balas ke pesan sticker")


@app.on_message(filters.command("mmf", PREFIX) & filters.me)
async def mmfsticker(client, message):
    r=message.reply_to_message
    auah=get_arg(message)
    if r and auah:
        try:
            await message.edit("Yo menambahkan text di sticker")
            oh=await r.forward("@PrimeMegaBot")
            kon=await oh.reply(f"/mmf {auah}")
            await asyncio.sleep(7)
        except YouBlockedUser:
            await app.unblock_user("@PrimeMegaBot")
            await message.edit("Yo menambahkan text di sticker")
            await app.send_message("@PrimeMegaBot", "/start")
            oh=await r.forward("@PrimeMegaBot")
            kon=await oh.reply(f"/mmf {auah}")
            await asyncio.sleep(7)
        async for tiny in app.search_messages("@PrimeMegaBot", limit=1):
            if tiny:
                await message.delete()
                await message.reply_sticker(sticker=tiny.sticker.file_id, reply_to_message_id=message.reply_to_message.id)
            else:
                await message.edit("Sepertinya ada yang salah")
                
            await oh.delete()
            await kon.delete()
            await tiny.delete()
    else:
        return await message.edit("Silahkan balas ke pesan dan kombinasi dengan text atas;bawah")

@app.on_message(filters.command("togif", PREFIX) & filters.me)
async def togifsticker(client, message):
    chat = message.chat.id
    rp = message.reply_to_message
    if rp:
        await message.edit("Processing")
        anu = await app.download_media(rp, "prime.gif")
        await app.send_animation(chat, anu, reply_to_message_id=message.reply_to_message.id)
        await message.delete()
        os.remove(anu)
    else:
        await message.edit("Silahkan balas ke sticker animasi video")
        
