# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

from pyrogram import filters

from config import LOGO_PRIME, PREFIX
from Prime import CMD_HELP, HELP, app
from Prime.helpers.pyrohelper import get_arg
from prettytable import PrettyTable


def split_list(input_list, n):
    n = max(1, n)
    return [input_list[i : i + n] for i in range(0, len(input_list), n)]
    


@app.on_message(filters.command("help", PREFIX) & filters.me)
async def help(client, message):
    args = get_arg(message)
    if not args:
        tai = "Available Commands\n"
        ppk = "\n**Support:** @PrimeSupportGroup\n**Patner:**@kenkanasw"
        ac = PrettyTable()
        ac.header = False
        ac.title = "✨ PRIME-USERBOT ✨"
        ac.align = "l"
        for x in split_list(sorted(CMD_HELP.keys()), 2):
          ac.add_row([x[0], x[1] if len(x) >= 2 else None])
        await message.edit(tai + f"```{str(ac)}```" + ppk)
        await message.reply(f"Contoh menggunakannya `{PREFIX}help asupan`")
        return
    else:
        kontol = "\n@PrimeSupportGroup\n@kenkanasw"
        tai = "✨ PRIME-USERBOT ✨\n"
        module_help = CMD_HELP.get(args, False)
        if not module_help:
            await message.edit(f"__Sepertinya tidak ada modul {args}.__")
            return
        else:
            await message.edit(tai + module_help + kontol)
