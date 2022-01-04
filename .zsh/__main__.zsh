role="${${${(%):-%N}:t}[2,-1]}"

# echo "> $role"

export ZDOTDIR="$HOME/.zsh"

for script in $ZDOTDIR/hook/$role/*; do
	# echo "> HK $script"
	source "$script"
done

for script in $ZDOTDIR/plugin/*/*.$role; do
	pushd "$(dirname "$script")"
	# echo "> CB $script"
	# echo "> PWD $(pwd)"
	source "$script"
	popd
done

unset role script

[ -f ~/.travis/travis.sh ] && source ~/.travis/travis.sh

PATH="~/.local/bin:/usr/local/sbin:${PATH}"
export PATH
