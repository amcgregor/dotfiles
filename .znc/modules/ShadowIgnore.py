# Copyright (c) 2020 Alice Bevan-McGregor.  Pre-released under an MIT license.

# https://modern.ircdocs.horse/formatting.html

import os

import znc
from znc import COptionalTranslation as _


class ShadowIgnore(znc.Module):
	"""An implementation of moderation-friendly shadow-/ignore; message masking without actual hiding.
	
	For use when actually /ignoring the user may inhibit the ability to perform required moderation duties if that
	user becomes problematic. The intent is to still be aware that they are posting messages, without the need to dig
	into logs to see what they might be saying, if actually required.
	
	Arguments are the nicknames to automatically prefix with a "spoiler" formatting token.
	"""
	
	module_types = [znc.CModInfo.UserModule]
	has_args = True
	args_help_text = "The nicknames to mask."
	description = "Automatically mark messages from certain users as spoilers."
	
	def OnLoad(self, args, message):
		"""Preserve the argument list as the list of nicknames to mask."""
		
		self.ignores = str(args).split()
		self.PutModule(f"Messages from {','.join(self.ignores)} will be hidden.")
		
		# This dance is ludicrous.
		
		def Help(line): self.OnHelp(line)
		def AddNick(line): self.OnAddNick(line)
		def RemoveNick(line): self.OnRemoveNick(line)
		def ListNicks(line): pass
		
		self.commands.append(("Help", _(""), _("Displays this help message describing this module's commands."), Help))
		self.commands.append(("AddNick", _("<nick>"), _("Add a nick to the shadow ignore list."), AddNick))
		self.commands.append(("RemoveNick", _("<nick>"), _("Remove a nickname from the ignored list."), RemoveNick))
		self.commands.append(("ListNicks", _(""), _("Display the list of currently ignored nicks."), ListNicks))
		
		return True
	
	def OnModCommand(self, line):
		args = line.split(None, 1)
		if not args: return True
		
		cmd = args[0]
		line = args[1] if len(args) > 1 else None
		
		for cmdName, args, description, function in self.commands:
			if cmdName.lower() == cmd.lower(): # no need for case sensitivity
				function(line)
				break
		
		return True
	
	def OnChanTextMessage(self, Message):
		"""Match 'ignored' users, and modify incoming messages from them."""
		
		if Message.GetNick().lower() in self.ignores:
			self.PutModule(f"Message from {message.GetNick()} hidden.")
			Message.SetText(f'\x031,1{message.GetText()}\x0f')
		
		return znc.CONTINUE
	
	def OnAddNick(self, line):
		self.PutModule(f"Added nick: {line}")
