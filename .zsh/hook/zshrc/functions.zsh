# Alice's over-engineered z-shell configuration, released in the public domain.
# Standard function configuration and definitions.

# Dynamic function loading path.
fpath+=($ZDOTDIR/func)

# Load the functions.
for name in ${ZDOTDIR}/func/*; do
	autoload $name
done

# Great thanks to Valodim in #zsh for his assistance with this!
parent() { [[ ${1[1,$#2]} == $2 ]] }
sibling() { [[ ${1:a:h} == ${2:a:h} ]]  }

# We do a few things every time the user changes directory.
# * If we are in a virtual environment, check to see if we have left it and deactivate.
# * If we are still in a virtual environment, stop processing.
# * Check to see if we just entered a virtual environment; if so, activate.
# * If we just activated a new venv, check for a src folder and enter it if one exists.
function chpwd() {
	emulate -L zsh
	
	ls
	
	# Automatically fetch remotes and display Git status information when entering a repository.
	if [[ -d .git ]]; then
		clear
		git fetch -q
		ugst
	fi
	
	# Handle transitioning out of a virtual nevironment root.
	[[ -n $VIRTUAL_ENV ]] && [[ -n $VIRTUAL_ROOT ]] || { parent $PWD $VIRTUAL_ENV || deactivate }
	[[ -n $VIRTUAL_ENV ]] && [[ -n $VIRTUAL_ROOT ]] && { parent $PWD $VIRTUAL_ROOT || deactivate }
	[[ -n $VIRTUAL_ENV ]] && return
	
	# Activate any environment we transition into.
	[[ -e .venv/bin/activate ]] && export VIRTUAL_ROOT="$PWD" && source .venv/bin/activate
	[[ -e bin/activate ]] && source bin/activate
	[[ -e src ]] && cd src
}
