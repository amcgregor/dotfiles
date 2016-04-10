# Alice's over-engineered z-shell configuration.
# Line editing specific options.

bindkey -v  # Vim master race.

export KEYTIMEOUT=1  # Reduce the <ESC> timeout to 0.1 seconds.

# Use vim cli mode
bindkey '^P' up-history
bindkey '^N' down-history

# backspace and ^h working even after
# returning from command mode
bindkey '^?' backward-delete-char
bindkey '^h' backward-delete-char

# ctrl-w removed word backwards
bindkey '^w' backward-kill-word

# ctrl-r starts searching history backward
bindkey '^r' history-incremental-search-backward

