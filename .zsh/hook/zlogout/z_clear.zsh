# Automatically clear interactive sessions, if local.

[[ -o interactive ]] || return

# Clear the console if it is a local terminal
case `tty` in
	/dev/tty[0-9]*|/dev/ttyS[0-9]*)
		[[ -x /usr/bin/clear_console ]] && /usr/bin/clear_console --quiet || clear
		;;
	*)
		echo "Bye, bye, $LOGNAME!"
		echo
esac
