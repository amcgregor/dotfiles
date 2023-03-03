if [[ -e /opt/homebrew ]]; then
	export HOMEBREW_NO_ENV_HINTS=1
	
	eval "$(/opt/homebrew/bin/brew shellenv)"
	
	alias brewup='clear; brew update; clear; brew outdated; echo -en "Proceed? "; read; clear; brew upgrade'
fi
