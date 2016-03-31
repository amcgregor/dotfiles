# Alice's over-engineered z-shell configuration, released in the public domain.
# Primary loader for categories of common and not-so-common shell aliases.

for script in $ZDOTDIR/hook/alias/*; do
	# echo "> HK $script"
	source "$script"
done

