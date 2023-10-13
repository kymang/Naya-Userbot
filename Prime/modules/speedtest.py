# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
#
# All rights reserved.

import os
import asyncio
import speedtest
from datetime import datetime

import psutil
from psutil._common import bytes2human
from asyncio import sleep

from pyrogram import filters

from config import LOG_CHAT, PREFIX
from Prime import CMD_HELP, app


CMD_HELP.update(
  {
    "speed": f"""
『 **Speed** 』
  `{PREFIX}speed` -> Cek speed server kamu.
  `{PREFIX}sysinfo -> Untuk melihat info system
"""
  }
)

def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit("Running Download SpeedTest")
        test.download()
        m = m.edit("Running Upload SpeedTest")
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit("Sharing SpeedTest Results")
    except Exception as e:
        return m.edit(e)
    return result

@app.on_message(filters.command("speed", PREFIX) & filters.me)
async def speed(client, message):
    m = await message.edit("Running Speed test")
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m)
    output = f"""**Speedtest Results**
      
<u>**Client:**</u>
**__ISP:__** {result['client']['isp']}
**__Country:__** {result['client']['country']}
  
<u>**Server:**</u>
**__Name:__** {result['server']['name']}
**__Country:__** {result['server']['country']}, {result['server']['cc']}
**__Sponsor:__** {result['server']['sponsor']}
**__Latency:__** {result['server']['latency']}  
**__Ping:__** {result['ping']}"""
    await app.send_photo(message.chat.id, photo=result["share"], caption=output)
    await m.delete()

async def generate_sysinfo(workdir):
    # uptime
    info = {
        'BOOT': (datetime.fromtimestamp(psutil.boot_time())
                 .strftime("%Y-%m-%d %H:%M:%S"))
    }
    # CPU
    cpu_freq = psutil.cpu_freq().current
    if cpu_freq >= 1000:
        cpu_freq = f"{round(cpu_freq / 1000, 2)}GHz"
    else:
        cpu_freq = f"{round(cpu_freq, 2)}MHz"
    info['CPU'] = (
        f"{psutil.cpu_percent(interval=1)}% "
        f"({psutil.cpu_count()}) "
        f"{cpu_freq}"
    )
    # Memory
    vm = psutil.virtual_memory()
    sm = psutil.swap_memory()
    info['RAM'] = (f"{bytes2human(vm.total)}, "
                   f"{bytes2human(vm.available)} available")
    info['SWAP'] = f"{bytes2human(sm.total)}, {sm.percent}%"
    # Disks
    du = psutil.disk_usage(workdir)
    dio = psutil.disk_io_counters()
    info['DISK'] = (f"{bytes2human(du.used)} / {bytes2human(du.total)} "
                    f"({du.percent}%)")
    if dio:
        info['DISK I/O'] = (f"R {bytes2human(dio.read_bytes)} | W {bytes2human(dio.write_bytes)}")
    # Network
    nio = psutil.net_io_counters()
    info['NET I/O'] = (f"TX {bytes2human(nio.bytes_sent)} | RX {bytes2human(nio.bytes_recv)}")
    # Sensors
    sensors_temperatures = psutil.sensors_temperatures()
    if sensors_temperatures:
        temperatures_list = [
            x.current
            for x in sensors_temperatures['coretemp']
        ]
        temperatures = sum(temperatures_list) / len(temperatures_list)
        info['TEMP'] = f"{temperatures}\u00b0C"
    info = {f"{key}:": value for (key, value) in info.items()}
    max_len = max(len(x) for x in info)
    return ("```"
            + "\n".join([f"{x:<{max_len}} {y}" for x, y in info.items()])
            + "```")



@app.on_message(filters.command("sysinfo", PREFIX) & filters.me)
async def sysinfo_text(client, message):
   await message.edit("Mendapatkan informasi sistem ...")
   response = await generate_sysinfo(app.workdir)
   await message.edit("<u>**System Information**</u>:\n" + response)
