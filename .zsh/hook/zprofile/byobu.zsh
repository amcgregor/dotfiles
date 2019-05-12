[[ -o interactive ]] || return

[[ -x /usr/bin/byobu-launch ]] || [[ -x /usr/local/bin/byobu-launch ]] || return

[[ -e /usr/local/bin/python3 ]] && export BYOBU_PYTHON="/usr/local/bin/python3"
[[ ! -e ~/.no-byobu ]] || return

[[ $TTY == /dev/tty([sS]|)<-> ]] || return

_byobu_sourced=1 . $(which byobu-launch)

