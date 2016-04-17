# Alice's over-engineered z-shell configuration, released in the public domain.

ZSH_HIGHLIGHT_HIGHLIGHTERS=(main brackets pattern cursor)

source "$ZDOTDIR/plugin/highlight/zsh-syntax-highlighting.zsh"

ZSH_HIGHLIGHT_PATTERNS+=('rm -rf' 'fg=black,bg=red')



