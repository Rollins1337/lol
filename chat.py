# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
""" Userbot module containing userid, chatid and log commands"""

from time import sleep

from telethon.tl.functions.channels import LeaveChannelRequest

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern="^.userid$")
async def useridgetter(target):
    """ For .userid command, returns the ID of the target user. """
    message = await target.get_reply_message()
    if message:
        if not message.forward:
            user_id = message.sender.id
            if message.sender.username:
                name = "@" + message.sender.username
            else:
                name = "**" + message.sender.first_name + "**"

        else:
            user_id = message.forward.sender.id
            if message.forward.sender.username:
                name = "@" + message.forward.sender.username
            else:
                name = "*" + message.forward.sender.first_name + "*"
        await target.edit("**__Name:__** {} \n**__User ID:__** **__{}**__".format(
            name, user_id))


@register(outgoing=True, pattern="^.chatid$")
async def chatidgetter(chat):
    """ For .chatid, returns the ID of the chat you are in at that moment. """
    await chat.edit("**__Chat ID:__**\n**__" + str(chat.chat_id) + "**__")


@register(outgoing=True, pattern=r"^.log(?: |$)([\s\S]*)")
async def log(log_text):
    """ For .log command, forwards a message
     or the command argument to the bot logs group """
    if BOTLOG:
        if log_text.reply_to_msg_id:
            reply_msg = await log_text.get_reply_message()
            await reply_msg.forward_to(BOTLOG_CHATID)
        elif log_text.pattern_match.group(1):
            user = f"#LOG / Chat ID: {log_text.chat_id}\n\n"
            textx = user + log_text.pattern_match.group(1)
            await bot.send_message(BOTLOG_CHATID, textx)
        else:
            await log_text.edit("**__What am I supposed to log?**__")
            return
        await log_text.edit("**__Logged Successfully**__")
    else:
        await log_text.edit("**__This feature requires Logging to be enabled!**__")
    sleep(2)
    await log_text.delete()


@register(outgoing=True, pattern="^.kickme$")
async def kickme(leave):
    """ Basically it's .kickme command """
    await leave.edit("**__Nope, no, no, I go away**__")
    await bot(LeaveChannelRequest(leave.chat_id))


CMD_HELP.update({"chatid": "Fetch the current chat's ID"})
CMD_HELP.update({
    "userid":
    "Fetch the ID of the user in reply or the "
    "original author of a forwarded message."
})
CMD_HELP.update(
    {"log": "Forward the message you've replied to to your "
     "botlog group."})
CMD_HELP.update({"kickme": "Leave from a targeted group."})
