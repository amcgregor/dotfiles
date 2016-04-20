# Alice's over-engineered z-shell configuration, released in the public domain.
# Boy howdy does zsh have a lot of options.

setopt auto_cd # Typing the name of a subdirectory of the CWD (or in cdpath) will go there.
setopt auto_pushd # Automatically append to the stack.
setopt cdable_vars

setopt extended_glob
setopt interactive_comments # Allow comments in interactive shells.
setopt list_packed
setopt list_types
setopt long_list_jobs
setopt magic_equal_subst
setopt multibyte
setopt NO_c_bases
setopt NO_complete_aliases
setopt NO_hup
setopt NO_list_rows_first
setopt NO_numeric_glob_sort
setopt NO_path_dirs
setopt null_glob
setopt pushd_ignore_dups # Ignore duplicate directories in the stack.
setopt pushd_minus # Reverse the meaning of +/- after pushing the CWD.
setopt pushd_to_home # With no arguments act like 'pushd $HOME'.
setopt pushdsilent
setopt rc_quotes
setopt transientrprompt

unsetopt flow_control

typeset -A shellopts

shellopts[screen_names]=1 # Dynamically change window names in GNU screen
shellopts[titlebar]=1     # Whether the titlebar can be dynamically changed
shellopts[utf8]=1         # Set up a few programs for UTF-8 mode

cdpath=(. $HOME/Projects $HOME/app $HOME/apps)
watch=(notme)

typeset -U cdpath watch

LOGCHECK=60
REPORTTIME=2
WATCHFMT='%n %a %l from %m at %t.'

export EDITOR='vim'
export VISUAL=$EDITOR
export LESSOPEN="|lesspipe.sh %s"


# Enable the definition of standard color codes.
autoload -U colors
colors

setopt vi

