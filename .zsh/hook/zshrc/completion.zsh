# Alice's over-engineered z-shell configuration, released in the public domain.
# Completion configuration.

# Add the external completions to the function auto-import path.
fpath+=($ZDOTDIR/plugin/comp/src)

setopt always_to_end
setopt auto_menu # Cycle through possibilities during tab completion.
setopt complete_in_word # Completion matches text to the left of the cursor when mid-word.
setopt glob_complete


# Configure our preferred completion rules.

zstyle ':completion:*:*:*:*:*' menu select

# Identify our own processes for kill and other commands that care.
zstyle ':completion:*:*:kill:*:processes' list-colors '=(#b) #([0-9]#) ([0-9a-z-]#)*=01;34=0=01'
zstyle ':completion:*:*:*:*:processes' command "ps -u `whoami` -o pid,user,comm -w -w"

# Tab completion for path directories on cd, disabling named-directories completion.
zstyle ':completion:*:cd:*' tag-order local-directories directory-stack path-directories
