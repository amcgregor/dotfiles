# Alice's over-engineered z-shell configuration, released in the public domain.
# Primary loader for categories of common and not-so-common shell aliases.

# Load all aliases.
for i in $(ls -b $ZDOTDIR/aliases); do
    load aliases/$(basename $i .zsh)
done
