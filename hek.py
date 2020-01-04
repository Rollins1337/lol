"""command: .hack"""

from telethon import events

import asyncio





@borg.on(events.NewMessage(pattern=".hack", outgoing=True))

async def _(event):

    if event.fwd_from:

        return

    animation_interval = 2

    animation_ttl = range(0, 11)



    animation_chars = [
        
            "**__Connecting To Hacked Private Server...**__",
            "**__Target Selected.**__",
            "**__Hacking... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ **__",
            "**__Hacking... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ **__",
            "**__Hacking... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ **__",    
            "**__Hacking... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ **__",
            "**__Hacking... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ **__",
            "**__Hacking... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ **__",
            "**__Hacking... 84%\n█████████████████████▒▒▒▒ **__",
            "**__Hacking... 100%\n█████████HACKED███████████ **__",
            "**__Targeted Account Hacked...\n\nPay 999$ To **__@Rollins1337**__ To Remove This Hack**__"
        ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await event.edit(animation_chars[i % 11])