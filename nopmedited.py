# -*- coding: future_fstrings -*-

#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .. import loader, utils

import logging

from telethon import functions, types
logger = logging.getLogger(__name__)


def register(cb):
    cb(AntiPMMod())


class AntiPMMod(loader.Module):
    """Prevents people sending you unsolicited private messages"""
    def __init__(self):
        self.name = _("Anti PM")
        self.config = loader.ModuleConfig("PM_BLOCK_LIMIT", None, "Max number of PMs before user is blocked, or None")
        self._me = None
        self._ratelimit = []
        self.count = 0

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self._me = await client.get_me(True)

    async def blockcmd(self, message):
        """Block this user to PM without being warned"""
        user = await utils.get_target(message)
        if not user:
            await message.edit(_("**__Specify whom to block**__"))
            return
        await message.client(functions.contacts.BlockRequest(user))
        await message.edit(_("**__My owner doesn't want PM from**__ <a href='tg://user?id={}'>you</a> "
                             "**__so you have been blocked**__").format(user))

    async def unblockcmd(self, message):
        """Unlock this user to PM"""
        user = await utils.get_target(message)
        if not user:
            await message.edit(_("**__Specify whom to unblock **__"))
            return
        await message.client(functions.contacts.UnblockRequest(user))
        await message.edit(_("**__Alright fine! I'll forgive them this time. PM has been unblocked for **__ "
                             "<a href='tg://user?id={}'>this user</a>").format(user))

    async def allowcmd(self, message):
        """Allow this user to PM"""
        user = await utils.get_target(message)
        if not user:
            await message.edit(_("**__Who shall I allow to PM?**__"))
            return
        self._db.set(__name__, "allow", list(set(self._db.get(__name__, "allow", [])).union({user})))
        await message.edit(_("**__My owner has allowed**__ <a href='tg://user?id={}'>you</a> "
                             "**__to PM now**__").format(user))

    async def allowedcmd(self, message):
        """Shows the list of authorized users"""
        authorized = self._db.get(__name__, "allow")
        if not authorized:
        	await message.edit("**__No one is allowed to PM you so far**__")
        	return
        userlist = ""
        caption = "<b>Here are the users that are allowed to PM you:</b>\n\n"
        await message.edit("**__Retrieving the list, hold on a sec...**__")
        for user in authorized:
        	getuser = await self._client.get_entity(user)
        	userlist += "  »  <a href='tg://user?id={}'>{}</a>\n".format(user, str(getuser.first_name).capitalize())
        await message.edit(caption + userlist)
        
    async def clearallowedcmd(self, message):
    	"""Clears the list of authorized users"""
    	authorized = self._db.get(__name__, "allow")
    	if not authorized:
        	await message.edit("**__No one is allowed to PM you so far**__")
        	return
    	else:
        	authorized.clear()
        	self._db.get(__name__, "allow", authorized)
        	await message.edit("**__No one is allowed to PM you anymore**__")
        	return
        	
    async def reportcmd(self, message):
        """Report the user spam. Use only in PM"""
        user = await utils.get_target(message)
        if not user:
            await message.edit(_("**__Who shall I report?**__"))
            return
        self._db.set(__name__, "allow", list(set(self._db.get(__name__, "allow", [])).difference({user})))
        if message.is_reply and isinstance(message.to_id, types.PeerChannel):
            # Report the message
            await message.client(functions.messages.ReportRequest(peer=message.chat_id,
                                                                  id=[message.reply_to_msg_id],
                                                                  reason=types.InputReportReasonSpam()))
        else:
            await message.client(functions.messages.ReportSpamRequest(peer=message.to_id))
        await message.edit("**__You just got reported spam!!**__")

    async def denycmd(self, message):
        """Deny this user to PM without being warned"""
        user = await utils.get_target(message)
        if not user:
            await message.edit(_("**__Who shall I deny to PM?**__"))
            return
        self._db.set(__name__, "allow", list(set(self._db.get(__name__, "allow", [])).difference({user})))
        await message.edit(_("**__My owner has denied**__ <a href='tg://user?id={}'>you</a> "
                             "**__of your PM permissions.**__").format(user))

    async def notifoffcmd(self, message):
        """Disable the notifications from denied PMs"""
        self._db.set(__name__, "notif", True)
        await message.edit(_("**__Notifications from denied PMs are silenced.**__"))

    async def notifoncmd(self, message):
        """Disable the notifications from denied PMs"""
        self._db.set(__name__, "notif", False)
        await message.edit(_("**__Notifications from denied PMs are now activated.**__"))

    async def setlimitcmd(self, message):
        """Sets a message limit to auto-block"""
        count = utils.get_args_raw(message)
        if not count.isdigit():
        	await message.edit("**__Enter an actual number**__")
        	return
        else:
        	if int(count) < 2:
        		await message.edit("**__Value has to be higher than 1**__")
        		return
        	else:
        		self._db.set(__name__, "msglimit", int(count))
        		await message.edit(_("**__Maximum message limit has been successfully set to " + str(count) + ".**__"))
    
    async def watcher(self, message):
        if getattr(message.to_id, "user_id", None) == self._me.user_id:
            logger.debug("pm'd!")
            user = await utils.get_user(message)
            if user.is_self or user.bot or user.verified:
                logger.debug("User is self, bot or verified.")
                return
            if self.get_allowed(message.from_id):
                logger.debug("Authorised pm detected")
            else:
                await message.respond(_("**__Hey there! Unfortunately, I don't accept private messages from "
                                        "strangers.\n\nPlease contact me in a group, or wait**__"
                                        "**__for me to approve you.**__"))
                max = self._db.get(__name__, "msglimit")
                self.count += 1
                if self.count >= max:
                	await message.respond(_("**__Hey! I don't appreciate you barging into my PM like this! "
                	"Did you even ask me for approving you to PM? No? Goodbye then."
                	"\n\nAh btw, you've been reported as spam already.**__"))
                	await message.client(functions.contacts.BlockRequest(message.from_id))
                	await functions.message.ReportSpamRequest(message.chat_id)
                	limit.clear()
                if self._db.get(__name__, "notif", False):
                    await message.client.send_read_acknowledge(message.chat_id)

    def get_allowed(self, id):
        return id in self._db.get(__name__, "allow", [])
