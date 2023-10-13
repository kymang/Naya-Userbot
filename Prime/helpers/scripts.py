# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

import traceback
from pyrogram import errors

def format_exc(e: Exception, hint: str = None):
    traceback.print_exc()
    if isinstance(e, errors.RPCError):
        return (
            f"<b>Telegram API error!</b>\n"
            f"<code>[{e.CODE} {e.ID or e.NAME}] - {e.MESSAGE}</code>"
        )
    else:
        if hint:
            hint_text = f"\n\n<b>Hint: {hint}</b>"
        else:
            hint_text = ""
        return (
            f"<b>Error!</b>\n" f"<code>{e.__class__.__name__}: {e}</code>" + hint_text
        )
