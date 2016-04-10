# Alice's over-engineered z-shell configuration, released in the public domain.
# We allow a few vim commands to be executed, having them "do the right thing".

if [[ -e /Applications/Third-Party/MacVim.app ]]; then
	alias :e='open -a MacVim'
else
	alias :e='vim'
fi

