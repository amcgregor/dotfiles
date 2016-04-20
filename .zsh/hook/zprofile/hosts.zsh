# Alice's over-engineered z-shell configuration, released in the public domain.
# Hostname lookup, notably for use in completions.

if [[ ! -e $HOME/.ssh ]]; then
	mkdir $HOME/.ssh
	chmod 700 $HOME/.ssh
fi

if [[ ! -e $HOME/.ssh/known_hosts ]]; then
	touch $HOME/.ssh/known_hosts
	chmod 600 $HOME/.ssh/known_hosts
fi

# Initially, find everything in the system-level static hosts file.
# Then, add SSH known hosts to it.  We really want this file to exist, thus the preparation above.
[ -r /etc/ssh/ssh_known_hosts ] && _global_ssh_hosts=(${${${${(f)"$(</etc/ssh/ssh_known_hosts)"}:#[\|]*}%%\ *}%%,*}) || _ssh_hosts=()
[ -r ~/.ssh/known_hosts ] && _ssh_hosts=(${${${${(f)"$(<$HOME/.ssh/known_hosts)"}:#[\|]*}%%\ *}%%,*}) || _ssh_hosts=()
[ -r /etc/hosts ] && : ${(A)_etc_hosts:=${(s: :)${(ps:\t:)${${(f)~~"$(</etc/hosts)"}%%\#*}##[:blank:]#[^[:blank:]]#}}} || _etc_hosts=()
hosts=(
  "$_global_ssh_hosts[@]"
  "$_ssh_hosts[@]"
  "$_etc_hosts[@]"
  "$HOST"
  localhost
)

zstyle ':completion:*:hosts' hosts $hosts
