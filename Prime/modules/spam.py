# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

from asyncio import sleep

from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from config import LOG_CHAT, PREFIX
from Prime import CMD_HELP, app
from Prime.helpers.errors import Errors
from Prime.helpers.pyrohelper import get_arg

CMD_HELP.update(
    {
        "spam": f"""
『 **Spam** 』
  `{PREFIX}spam` -> Untuk mengirim spam ke teks tertentu.
  `{PREFIX}fspam` -> Untuk mengirim spam ke foto / video tertentu.
  `{PREFIX}delayspam` -> waktu jumlah isi pesan.
"""
    }
)


async def do_spam(limit, chat_id, spam_text=None, spam_message=None):
    # Sleep time (in seconds)
    sleep_time = 0.1 if limit <= 50 else 0.5 if limit <= 100 else 1
    spm_limit = int(limit)
    try:
        # Saves message in the log channel
        if spam_message:
            msg = await spam_message.copy(LOG_CHAT)
        for i in range(0, spm_limit):
            if spam_text:
                await app.send_message(chat_id, spam_text)
            elif msg:
                await msg.copy(chat_id)
            else:
                return
            await sleep(sleep_time)
        try:
            await msg.delete()
        except:
            pass
    except FloodWait as e:
        await sleep(e.x)
        return await do_spam(limit, chat_id, spam_text=None, spam_message=None)
    except BaseException as e:
        raise Errors.SpamFailed(e)


@app.on_message(filters.command("spam", PREFIX) & filters.me)
async def spam_text(client, message):
    spm_msg = await message.edit_text("`Processing...`")
    r_msg = message.reply_to_message
    args = get_arg(message)
    spam_limit = 10
    if r_msg:
        # Checks if the replied message has any text
        if not r_msg.text:
            return await spm_msg.edit(
                f"Balas pesan teks untuk mengirim spam!\n\nApakah maksud Anda `{PREFIX}fspam` ?"
            )
        to_spam = r_msg.text
        # Checks if spam limit is provided by the user
        if args and args.isnumeric():
            spam_limit = int(args)
    elif args:
        splt_args = args.split(None, 1)
        if len(splt_args) < 2:
            return await spm_msg.edit(
                "Berikan beberapa teks atau balas pesan teks untuk mengirim spam!"
          )
        to_spam = splt_args[1]
        if splt_args[0].isnumeric():
            spam_limit = int(splt_args[0])
    else:
        return await spm_msg.edit(
                "Berikan beberapa teks atau balas pesan teks untuk mengirim spam!"
           )
    await do_spam(spam_limit, message.chat.id, spam_text=to_spam)
    await spm_msg.edit(f"`Sukses spammed {spam_limit} messages!`")


@app.on_message(filters.command("fspam", PREFIX) & filters.me)
async def copy_spam(_, message: Message):
    spm_msg = await message.edit_text("`Processing...`")
    r_msg = message.reply_to_message
    args = get_arg(message)
    spam_limit = 10
    if r_msg:
        # Checks if spam limit is provided by the user
        if args and args.isnumeric():
            spam_limit = int(args)
    else:
        return await spm_msg.edit("Balas pesan ke media untuk spam media!")
    await do_spam(spam_limit, message.chat.id, spam_message=r_msg)
    await spm_msg.edit(f"`Successfully spammed {spam_limit} messages!`")

@app.on_message(filters.command("delayspam", PREFIX) & filters.me)
async def delayspam(client, message):
    chat = message.chat.id
    prime = "".join(message.text.split(maxsplit=1)[1:]).split(" ", 2)
    userbot = prime[1:]
    waktu = float(prime[0])
    jumlah = int(userbot[0])
    pesan = str(userbot[1])
    kk = await message.edit(f"Memulai delayspam jumlah pesan {jumlah} dengan waktu {waktu}")
    for _ in range(jumlah):
        await app.send_message(chat, pesan)
        await sleep(waktu)
        await kk.delete()
            
    return await app.send_message(chat, f"Berhasil delayspam jumlah {jumlah} waktu {waktu}")
