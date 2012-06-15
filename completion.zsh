# Alice's over-engineered z-shell configuration, released in the public domain.
# Completion tweaks.

# Load hostnames from /etc/hosts and ~/.ssh/known_hosts.
hosts=($(cat /etc/hosts | grep -v "^#" | awk '{print $1}'| cut -d"," -f1), $(cat $HOME/.ssh/known_hosts | awk '{print $1}'| cut -d"," -f1))
zstyle ':completion:*' hosts $hosts

fpath=($ZDOTDIR/comp $fpath)
