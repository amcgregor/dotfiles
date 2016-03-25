# Alice's over-engineered z-shell configuratdion.
# Verify if our dotfiles are up-to-date.

# We only attempt this check for interactive sessions.

[[ -o interactive ]] || return


# Also skip the check if the home folder isn't dotfiles-managed.

[[ -d ~/.dotfiles ]] || return


function ebegin () {
	echo -en " \033[1;32m*\033[0m $1... "
}

function eend () {
	local integer result=${1:=$?}
	local message="${2:=failed}"
	
	[[ $result -eq 0 ]] && echo -e "\b\b\b\b: done." || echo -e "\b\b\b\b: ${message}."
	
	return 0
}


# Calculate if we have diverged from upstream.

# TODO: Limit check to once per day.

ebegin "Checking for dotfiles update"

ours=`env GIT_DIR="${HOME}/.dotfiles" git rev-parse HEAD`
theirs=`env GIT_DIR="${HOME}/.dotfiles" git ls-remote origin -h refs/heads/dotfiles`

[[ "$ours" == "$theirs[(w)1]" ]] && eend || eend 1 "an update is availble"

unset ours theirs

