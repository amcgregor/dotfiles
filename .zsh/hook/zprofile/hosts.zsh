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
# Then, add SSH known hosts to it.  We need this file to exist, thus the preparation above.
hosts=( \
	$(cat /etc/hosts | grep -v "^#" | awk '{print $1}' | cut -d"," -f1), \
	$(cat $HOME/.ssh/known_hosts | awk '{print $1}' | cut -d"," -f1) \
)

