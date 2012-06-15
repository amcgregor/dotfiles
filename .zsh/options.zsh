# Alice's over-engineered z-shell configuration, released in the public domain.
# Boy howdy does zsh have a lot of options.

setopt always_to_end
setopt auto_cd # Typing the name of a subdirectory of the CWD (or in cdpath) will go there.
setopt auto_menu # Cycle through possibilities during tab completion.
setopt auto_pushd # Automatically append to the stack.
setopt cdable_vars
setopt complete_in_word # Completion matches text to the left of the cursor when mid-word.
# setopt correct # Correct spelling as needed. Update cache with 'hash -r'.
setopt extended_glob
setopt glob_complete
setopt interactive_comments # Allow comments in interactive shells.
setopt interactive_comments # Allow comments in the interactive shell.
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

unsetopt flow_control