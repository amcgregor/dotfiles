role="${${${(%):-%N}:t}[2,-1]}"

export ZDOTDIR="$HOME/.zsh"

for script in $ZDOTDIR/hook/$role/*; do
	source "$script"
done

for script in $ZDOTDIR/plugin/*/*.$role; do
	pushd "$(dirname "$script")"
	source "$script"
	popd
done

unset role script

[ -f ~/.travis/travis.sh ] && source ~/.travis/travis.sh

PATH="~/.local/bin:/usr/local/sbin:${PATH}"
export PATH
