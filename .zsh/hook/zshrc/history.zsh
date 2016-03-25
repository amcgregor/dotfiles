# Alice's over-engineered z-shell configuration.
# History management-specific zsh options.

if [[ -z "$ZSH_CACHE_DIR" ]]; then
	echo "!! zshrc/history ZSH_CACHE_DIR Set this elsewhere."
	ZSH_CACHE_DIR="$HOME/.cache/zsh"
	
	# TODO: umask this private
	[[ ! -d "$ZSH_CACHE_DIR" ]] && mkdir -p $ZSH_CACHE_DIR
fi

if [[ -z "$HISTFILE" ]]; then
	# If there's an existing generic history file, use it.
	# Otherwise attempt to store a per-hostname history within the cache folder.
	# This allows my laptop to use one uninterrupted history despite renames while servers with shared homes are OK.
	if [[ -r "${ZDOTDIR:-$HOME}/.zsh_history" ]]; then
		HISTFILE="${ZDOTDIR:-$HOME}/.zsh_history"
	else
		if [[ ! -d "$ZSH_CACHE_DIR/history" ]]; then
			# TODO: umask this private
			mkdir -p "$ZSH_CACHE_DIR/history"
			chmod 700 "$ZSH_CACHE_DIR/history"
		fi
		
		HISTFILE="$ZSH_CACHE_DIR/history/$(hostname -f)"
	fi
	
	echo "HIST $HISTFILE"
fi

HISTSIZE=10000
SAVEHIST=10000

setopt append_history
setopt extended_history
setopt hist_expire_dups_first
setopt hist_find_no_dups
setopt hist_ignore_all_dups
setopt hist_ignore_dups
setopt hist_ignore_space
setopt hist_no_functions
setopt hist_no_store
setopt hist_reduce_blanks
setopt hist_save_no_dups
setopt hist_verify
setopt share_history
setopt inc_append_history

alias history='fc -il 1'
