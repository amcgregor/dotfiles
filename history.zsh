# Alice's over-engineered z-shell configuration, released in the public domain.
# History management-specific zsh options.

# Per-host history files are pretty epic and important when managing clusters.
HISTFILE=$ZDOTDIR/history/$(hostname -f)
HISTSIZE=10000
SAVEHIST=10000

setopt append_history
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
setopt share_history # Share history between multiple simultaneous zsh sessions.
setopt inc_append_history
