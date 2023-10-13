# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.


import traceback
from asyncio import get_running_loop
from inspect import getfullargspec
from io import BytesIO

from googletrans import Translator
from gtts import gTTS
from pyrogram import filters
from pyrogram.types import Message

from config import PREFIX
from Prime import CMD_HELP, app

CMD_HELP.update(
    {
        "trans": f"""
『 **Translate** 』
  `{PREFIX}tr` -> Translate message.
  `{PREFIX}tts` -> Ubah text ke voice.
"""
    }
)


async def edrep(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})


def convert(text):
    audio = BytesIO()
    i = Translator().translate(text, dest="id")
    lang = i.src
    tts = gTTS(text, lang=lang)
    audio.name = "Prime" + ".mp3"
    tts.write_to_fp(audio)
    return audio


@app.on_message(filters.command("tr", PREFIX) & filters.me)
async def translate(client, message):
    if len(message.command) != 2:
        return await message.edit_text(f"{PREFIX}tr [LANGUAGE_CODE]")
    lang = message.text.split(None, 1)[1]
    ah = Translator()
    if not message.reply_to_message or not lang:
        return await message.edit_text(
            f"Reply to a message with {PREFIX}tr [language code]"
        )
    reply = message.reply_to_message
    text = reply.text or reply.caption
    if not text:
        return await message.edit_text("Reply to a text to translate it")
    try:
        result = ah.translate(text, dest=lang)
        jembut = result.text
        asu = """**DITERJEMAHKAN**\n dari `{}` ke `{}`\n
        `{}`""".format(
            result.src, lang, jembut
        )
        await message.edit_text(asu)
    except Exception as exc:
        await message.edit_text(str(exc))


@app.on_message(filters.command("tts", PREFIX) & filters.me)
async def tts(client, message):
    if not message.reply_to_message:
        return await message.edit_text("Reply to some text ffs.")
    if not message.reply_to_message.text:
        return await message.edit_text("Reply to some text ffs.")
    m = await message.edit_text("Processing")
    text = message.reply_to_message.text
    try:
        loop = get_running_loop()
        audio = await loop.run_in_executor(None, convert, text)
        await message.reply_voice(audio)
        await m.delete()
        audio.close()
    except Exception as e:
        await m.edit(e)
        e = traceback.format_exc()
        print(e)
