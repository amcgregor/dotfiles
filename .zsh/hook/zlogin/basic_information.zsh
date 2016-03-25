# Alice's over-engineered z-shell configuration.
# Basic system information.

[[ -o interactive ]] || return

echo -en "\n \033[1;32m*\033[0m "
lsb_release -d -s | sed s/\"//g

echo -en " \033[1;32m*\033[0m "
uname -snmpr

MAX=$(($(cat /proc/cpuinfo | grep processor | wc -l) - 1))
LOAD=$(cat /proc/loadavg | cut -d '.' -f 1)

if [ $LOAD -gt $(($MAX * 4)) ]
then echo -en " \033[1;31m*\033[0m"
elif [ $LOAD -gt $MAX ]
then echo -en " \033[1;33m*\033[0m"
else echo -en " \033[1;32m*\033[0m"
fi
uptime

echo -en " \033[1;32m&\033[0m Network Interfaces: \033[1m"
ifconfig | grep "Link encap" | awk '{print $1}' | tr '\n' ' '
echo -e "\033[0m"

echo -en " \033[1;32m*\033[0m IPv4 Network Addresses: \033[1m"
ifconfig | grep "inet addr:" | cut -d: -f 2 | awk '{print $1}' | tr '\n' ' '
echo -e "\033[0m"

echo -en " \033[1;32m*\033[0m IPv6 Network Addresses: \033[1m"
ifconfig | grep "inet6 addr:" | awk '{print $3}' | tr '\n' ' '
echo -e "\033[0m"

