# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.


from pyrogram import filters, enums
from datetime import datetime
import aiohttp
from config import PREFIX
from Prime import app
from Prime.database.gmutedb import get_gmuted_users, gmute_user, ungmute_user
from Prime.helpers.pyrohelper import get_arg, Prime
from Prime.helpers.utils import eor

@app.on_message(filters.command("gmute", PREFIX) & filters.me)
async def gmute(_, message):
    reply = message.reply_to_message
    if reply:
        user = reply.User["id"]
    else:
        user = get_arg(message)
        if not user:
            await message.edit("**Siapa yang harus saya bungkam?**")
            return
    get_user = await app.get_users(user)
    await gmute_user(get_user.id)
    await message.edit(f"**Gmuted {get_user.first_name}, LOL!**")


@app.on_message(filters.command("ungmute", PREFIX) & filters.me)
async def gmute(_, message):
    reply = message.reply_to_message
    if reply:
        user = reply.User["id"]
    else:
        user = get_arg(message)
        if not user:
            await message.edit("**Siapa yang harus saya suarakan?**")
            return
    get_user = await app.get_users(user)
    await ungmute_user(get_user.id)
    await message.edit(f"**Unmuted {get_user.first_name}, enjoy!**")

@app.on_message(filters.command("stats", PREFIX) & filters.me)
async def stats(client, message):
    await message.edit_text("Collecting stats")
    start = datetime.now()
    u = 0
    g = 0
    sg = 0
    c = 0
    b = 0
    a_chat = 0
    Meh=await app.get_me()
    group = [enums.ChatType.SUPERGROUP, enums.ChatType.GROUP]
    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE:
            u += 1
        elif dialog.chat.type == enums.ChatType.BOT:
            b += 1
        elif dialog.chat.type == enums.ChatType.GROUP:
            g += 1
        elif dialog.chat.type == enums.ChatType.SUPERGROUP:
            sg += 1
            user_s = await dialog.chat.get_member(int(Meh.id))
            if user_s.status in (
                enums.ChatMemberStatus.OWNER,
                enums.ChatMemberStatus.ADMINISTRATOR,
            ):
                a_chat += 1
        elif dialog.chat.type == enums.ChatType.CHANNEL:
            c += 1

    end = datetime.now()
    ms = (end - start).seconds
    await message.edit_text(
        """**Statistik Anda Diperoleh dalam `{}` detik**\n\n
└ • **Anda memiliki `{}` Pesan Pribadi**.
└ • **Anda berada di `{}` Group.**
└ • **Anda berada di `{}` Super Group.**
└ • **Anda Berada di `{}` Channel.**
└ • **Anda Adalah Admin di `{}` Chat.**
└ • **Total Bot `{}`**""".format(
            ms, u, g, sg, c, a_chat, b
        )
    )

@app.on_message(filters.group & filters.incoming)
async def check_and_del(client, message):
    if not message:
        return
    try:
        if not message.from_user.id in (await get_gmuted_users()):
            return
    except AttributeError:
        return
    message_id = message.message_id
    try:
        await app.delete_messages(message.chat.id, message_id)
    except:
        pass  # you don't have delete rights


@app.on_message(filters.command("git", PREFIX) & filters.me)
async def github(client, message):
    if len(message.text.split()) == 1:
        await message.edit("Usage: `git (username)`")
        return
    username = message.text.split(None, 1)[1]
    URL = f"https://api.github.com/users/{username}"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await message.edit("`" + username +
                                        " Tidak di temukan`")

            result = await request.json()

            url = result.get("html_url", None)
            name = result.get("name", None)
            company = result.get("company", None)
            bio = result.get("bio", None)
            created_at = result.get("created_at", "Not Found")

            REPLY = (
                f"**GitHub Info untuk `{username}**`"
                f"\n**Username:** `{name}`\n**Bio:** `{bio}`\n**URL:** {url}"
                f"\n**Company:** `{company}`\n**Created at:** `{created_at}`"
            )

            if not result.get("repos_url", None):
                    return await message.edit(REPLY)
            async with session.get(result.get("repos_url", None)) as request:
                result = request.json
                if request.status == 404:
                    return await message.edit(REPLY)

                result = await request.json()

                REPLY += "\n**Repos:**\n"

                for nr in range(len(result)):
                    REPLY += f"[{result[nr].get('name', None)}]({result[nr].get('html_url', None)})\n"
                await message.edit(REPLY, disable_web_page_preview=True)

@app.on_message(filters.command("repo", PREFIX) & filters.me)
async def repo(client, message):
    toni = await app.get_users(1423479724)
    ken = await app.get_users(1607338903)
    await message.edit(Prime.REPO.format(toni.mention, ken.mention),
                       disable_web_page_preview=True)
                       
                       
@app.on_message(filters.command("deploy", PREFIX) & filters.me)
async def deploy(client, message):
    await message.edit(Prime.DEPLOY, 
    disable_web_page_preview=True)
