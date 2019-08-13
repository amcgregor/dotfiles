role="${${${(%):-%N}:t}[2,-1]}"

# echo "> $role"

export ZDOTDIR="$HOME/.zsh"

for script in $ZDOTDIR/hook/$role/*; do
	# echo "> HK $script"
	source "$script"
done

for script in $ZDOTDIR/plugin/*/*.$role; do
	cd "$(dirname "$script")"
	# echo "> CB $script"
	# echo "> PWD $(pwd)"
	source "$script"
done

unset role script

cd $HOME

[ -f ~/.travis/travis.sh ] && source ~/.travis/travis.sh

# Setting PATH for Python 3.6
# The original version is saved in .zprofile.pysave
PATH="/Library/Frameworks/Python.framework/Versions/3.6/bin:/usr/local/sbin:${PATH}"
export PATH
