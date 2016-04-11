[[ -o interactive ]] || return

[[ -x /usr/bin/byobu-launch ]] || [[ -x /usr/local/bin/byobu-launch ]] || return

[[ ! -e ~/.no-byobu ]] || return

_byobu_sourced=1 . $(which byobu-launch)

