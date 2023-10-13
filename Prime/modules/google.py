# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

import requests

from bs4 import BeautifulSoup
from googlesearch import search
from pyrogram import filters
from Prime import app, CMD_HELP
from config import PREFIX

def googlesearch(query):
    co=1
    returnquery={}
    for j in search(query, tld="co.in", num=10, stop=10, pause=2):
        url=str(j)
        response = requests.get(url)
        soup = BeautifulSoup(response.text , 'html.parser')
        metas = soup.find_all('meta')
        site_title=None
        for title in soup.find_all('title'):
            site_title=title.get_text()
        metadeta=[ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ]
        returnquery[co]={"title":site_title , "metadata":metadeta , "url":j}
        co=co+1
    return returnquery
  
@app.on_message(filters.command("google", PREFIX) & filters.me)  
async def gs(client, message):
    ah = await message.edit("Pencarian google")
    msg_txt=message.text 
    returnmsg=""
    query=None
    if " " in msg_txt:
        query=msg_txt[msg_txt.index(" ")+1:len(msg_txt)]
    else:
        await ah.edit("Give a query to search")
        return
    results=googlesearch(query)
    for i in range(1,6,1):
        presentquery=results[i]
        presenttitle=presentquery["title"]
        presentmeta=presentquery["metadata"]
        presenturl=presentquery["url"]
        print(presentquery)
        print(presenttitle)
        print(presentmeta)
        print(presenturl)
        if not presentmeta:
            presentmeta=""      
        else:
            presentmeta=presentmeta[0]
        returnmsg=returnmsg+f"[{str(presenttitle)}]({str(presenturl)})\n{str(presentmeta)}\n\n"
    await ah.edit(returnmsg, disable_web_page_preview=True)
    
CMD_HELP.update(
    {
        "google": f"""
『 **Google** 』
  `{PREFIX}google` -> Memulai mesin pencarian google
"""
    }
)
