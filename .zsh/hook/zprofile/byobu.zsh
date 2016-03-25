[[ -o interactive ]] || return

[[ -x /usr/bin/byobu-launch ]] || return

_byobu_sourced=1 . /usr/bin/byobu-launch

