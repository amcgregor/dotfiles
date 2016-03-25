# Set our fancy prompt, but only if running interactively.

[[ -o interactive ]] || return

. $ZDOTDIR/plugin/promptline/shell_prompt.sh
