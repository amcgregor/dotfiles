"""A ZNC Python module to improve the quality of service of Discord pseudo-federation.

Current home: https://gist.github.com/amcgregor/5724cb4cccf70468514da3bba7bbedba

A bot sits in the IRC channel and relays messages sent to the paired Discord channel. These messages are prefixed by
the Discord user's "nickname" with a "_discord" suffix within typical IRC "quoted message" angle brackets, e.g.:

	<Bridge> <GothAlice_discord> I am not a number!

This module rewrites incoming in-channel messages originating from the bridge (nickname configurable) and replaces the
apparent nickname of the message with that of the Discord user:

	<GothAlice> I am not a number!

Now IRC client features like nickname coloring, "highlight messages by", etc. can function seamlessly over the bridge,
and your own messages (if you have an account on both sides) will no longer trigger highlight notifications.

Drop this DiscordBridge.py file into your ZNC modules folder, e.g. ~/.znc/modules/, then issue the following command
within an IRC client connected to your ZNC instance.  "Pallets" is used as this is the original bridging bot this
module was written to be compatible with. Multiple nicknames may be provided, whitespace-separated.

	/msg *status LoadMod DiscordBridge Pallets

If the nickname of the bridge is ever altered, you can update the configuration of the module via the ZNC web
interface or by issuing this command in your IRC client:

	/msg *status ReloadMod DiscordBridge Potato

Due to a quirk in how messages are transferred, and differences in limitations on message length between the two
mediums, this module needs to track (for each channel and bot combination) the last-known bridged user's nick. This
is then used as the origin of messages from the bridge that are otherwise lacking attribution, i.e. they have been
wrapped.  (It does not do this yet.)

Copyright (c) 2020 Alice Bevan-McGregor.  Released under an MIT license.
"""


import os
import re
import typing

import znc
from znc import COptionalTranslation as _


# The message prefix added by the bridge. There is complexity in matching this, given an underscore is a valid
# character within a handle, as are parenthesis and other symbols, including most Unicode.
# This pattern matches as much word-like text (letters, numbers, etc., with Unicode-awareness) and consumes that
# as the handle to appear within the IRC buffer. Additional text beyond that is permitted when matching, but is not
# transferred.  Example:
#
# 	<Žan (casual)_discord> You can post links. 🙂
#
# In this situation, Žan would be a sufficient nickname match.  There are situations, though, where whitespace ought
# to be preserved, and transformed to make safe for IRC clients.  E.g.:
#
# 	<Alice McGregor_discord> Oh noes.
#
# Just matching "Alice" would be… insufficient.

prefix = re.compile(r'^<(?P<nick>[^>]+)(?:_discord)?>\s+', re.M | re.U)
#prefix = re.compile(r'^<[^z-Za-z0-9\u00C0-\u017F]*(?P<nick>[\w ]+)[\w()\[\]{} ]*(?:_discord)?>\s+', re.M | re.U)


class DiscordBridge(znc.Module):
	"""Make IRC bridging of Discord users more seamless.
	
	Matches messages conforming to the `prefix` pattern, removes that prefix, and takes the `nick` group as the
	nickname to replace the bridge's nickname.
	
	Because that's a lot of additional noise to add to logs, and disables IRC client behaviour re: nick coloring.
	
	Example lines: https://regex101.com/r/27iqiw/1
	"""
	
	_bridge_nicks: typing.Tuple[str, ...]
	_last_cache: typing.Dict[str, typing.Dict[str, str]]
	
	module_types = [znc.CModInfo.GlobalModule]  # znc.CModInfo.UserModule, znc.CModInfo.NetworkModule, ...
	has_args = True
	args_help_text = "The nickname of the Discord bridge."
	description = "Seamlessly masquerade bridged user's messages."
	
	def OnLoad(self, args, message):
		"""Preserve the argument list as the nickname to masquerade."""
		
		self._bridge_nicks = tuple(i.lower() for i in str(args).split())
		self._last_cache = {}
		
		self.PutModule(f"Messages delivered by {self._bridge_nicks} matching the bridge pattern will transparently masquerade.")
		
		return True
	
	def OnChanTextMessage(self, Message):
		"""Match the bridge and modify incoming messages to masquerade as the bridged user."""
		
		# Extract the information we require from the wrapped C structures.
		text = str(Message.GetText())
		nick = Message.GetNick()
		nick_ = str(nick)
		
		if nick_.lower() not in self._bridge_nicks: return znc.CONTINUE  # Skip non-bridge messages.
		match = prefix.match(text)  # Attempt to identify the forwarded sender.
		channel = Message.GetChan().GetName()
		cache = self._last_cache.setdefault(channel, {})
		
		if match:  # Update the last-known sender for this channel and bridge.
			cache[nick_] = match['nick'].replace(' ', '_').replace('_discord', '').strip()
			cache[nick_] = f"{cache[nick_]}̽"  # Note the Unicode combining character added to the end.
		
		nick.SetNick(cache[nick_])
		
		Message.SetNick(nick)  # Override the incoming sender.
		Message.SetText(prefix.sub("", text).strip())  # Override the incoming message.
		
		return znc.CONTINUE
