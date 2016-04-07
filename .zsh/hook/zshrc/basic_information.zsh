# Alice's over-engineered z-shell configuration.
# Basic system information.

[[ -o interactive ]] || return

if [[ -x /usr/bin/lsb_release ]]; then
	echo -en "\n \033[1;32m*\033[0m "
	lsb_release -d -s | sed s/\"//g
else
	echo -en "\n \033[1;32m*\033[0m "
	sysctl -n machdep.cpu.brand_string
	
	# TODO: system_profiler -detailLevel mini SPSoftwareDataType | grep Version | sed 's/^\s+//g' | tr '\n' '\000' | xargs -0 echo -en " \033[1;32m*\033[0m"
fi

echo -en " \033[1;32m*\033[0m "
uname -nmspr

if [[ -e /proc ]]; then

	MAX=$(($(cat /proc/cpuinfo | grep processor | wc -l) - 1))
	LOAD=$(cat /proc/loadavg | cut -d '.' -f 1)

	if [ $LOAD -gt $(($MAX * 4)) ]
	then echo -en " \033[1;31m*\033[0m"
	elif [ $LOAD -gt $MAX ]
	then echo -en " \033[1;33m*\033[0m"
	fi
fi

echo -en " \033[1;32m*\033[0m"
uptime

if [[ -e /proc ]]; then
	echo
	
	echo -en " \033[1;32m*\033[0m Network Interfaces: \033[1m"
	/sbin/ifconfig | grep "Link encap" | awk '{print $1}' | tr '\n' ' '
	echo -e "\033[0m"
	
	echo -en " \033[1;32m*\033[0m IPv4 Network Addresses: \033[1m"
	/sbin/ifconfig | grep "inet addr:" | cut -d: -f 2 | awk '{print $1}' | tr '\n' ' '
	echo -e "\033[0m"
	
	echo -en " \033[1;32m*\033[0m IPv6 Network Addresses: \033[1m"
	/sbin/ifconfig | grep "inet6 addr:" | awk '{print $3}' | tr '\n' ' '
	echo -e "\033[0m"
fi
