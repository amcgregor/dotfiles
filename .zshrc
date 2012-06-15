# Alice's over-engineered z-shell configuration, released in the public domain.
# Primary loader of external components.

# Update the path for all scripts regardless of interactivity.
path+=(/usr/local/bin /usr/bin /bin)

# The rest of this configuration applies to interactive shells only.
[[ -o nointeractive ]] && return

# Update the path for interactive execution.
path+=(/usr/local/sbin /usr/sbin /sbin)

# Explicit is better than implicit.
export ZDOTDIR="$HOME/.zsh"

# Helper function used within.
function load {
    source $ZDOTDIR/$1.zsh
}

# Chain load the various components of our configuration.
load oh-my-zsh
load shell
load variables
load functions
load aliases
load options
load bindings
load helpers
load history
load prompt
load completion
