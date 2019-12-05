"""command: .rape"""

from telethon import events

import asyncio





@borg.on(events.NewMessage(pattern=r"\.rape (.*)", outgoing=True))

async def fuck(event):

    if event.fwd_from:

        return

    animation_interval = 2

    animation_ttl = range(0, 11)

    input_str = event.pattern_match.group(1)

    if input_str == "rape":

        await event.edit(input_str)

        animation_chars = [
        
            "`Targeting Rape Victim...`",
            "`Victim Selected.`",
            "`Raping... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Raping... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Raping... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",    
            "`Raping... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Raping... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Raping... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Raping... 84%\n█████████████████████▒▒▒▒ `",
            "`Raping... 100%\n█████████RAPED███████████ `",
            "`Target Raped Successfully...\n\nPay 999$ To @mdfaiz6714355 or send real nudes of emma watson or get  Raped`"
        ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 11])
