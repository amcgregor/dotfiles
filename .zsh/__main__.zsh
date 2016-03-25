role="${${${(%):-%N}:t}[2,-1]}"

echo "> $role"

export ZDOTDIR="$HOME/.zsh"

typeset -U scripts
scripts=(
		"$ZDOTDIR/hook/$role/"*(N)
		"$ZDOTDIR/plugin/"*.$role(N)
	)

for script in $ZDOTDIR/hook/$role/*; do
	echo "> HK $script"
	source "$script"
done

for script in $ZDOTDIR/plugin/*/*.$role; do
	cd "$(dirname "$script")"
	echo "> CB $script"
	echo "> PWD $pwd"
	source "$script"
done

unset role scripts

cd $HOME
