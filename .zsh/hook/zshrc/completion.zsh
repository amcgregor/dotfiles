# Alice's over-engineered z-shell configuration, released in the public domain.
# Completion configuration.

# Add the external completions to the function auto-import path.
fpath+=($ZDOTDIR/plugin/comp/src)

setopt always_to_end
setopt auto_menu # Cycle through possibilities during tab completion.
setopt complete_in_word # Completion matches text to the left of the cursor when mid-word.
setopt glob_complete

