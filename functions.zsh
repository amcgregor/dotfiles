# Alice's over-engineered z-shell configuration, released in the public domain.
# Dynamically loaded functions.

fpath=($ZDOTDIR/func $fpath)

# We do a few things every time the user changes directory.
# First, run ls.  I do this so often manually that it's stupid.
# Second, check to see if we just entered a virtual environment; if so, activate.
function chpwd() {
    emulate -L zsh
    [[ -e bin/activate ]] && source bin/activate
}
