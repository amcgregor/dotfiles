role="${${${(%):-%N}:t}[1,-1]}"

export ZDOTDIR="$HOME/.zsh"

typeset -U scripts
scripts=(
		"$ZDOTDIR/hook/$role/"*(N)
		"$ZDOTDIR/plugin/"*.$role(N)
	)

for script in $(ls -b $ZDOTDIR/hook/$role/* $ZDOTDIR/plugin/*/*.$role); do
	source "$script"
done

unset role scripts
