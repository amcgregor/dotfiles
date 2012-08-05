# Alice's over-engineered z-shell configuration, released in the public domain.
# Dynamically loaded functions.

fpath=($ZDOTDIR/func $fpath)

# Great thanks to Valodim in #zsh for his assistance with this!
parent() { [[ ${1[1,$#2]} == $2 ]] }
sibling() { [[ ${1:a:h} == ${2:a:h} ]]  }

# We do a few things every time the user changes directory.
# * If we are in a virtual environment, check to see if we have left it and deactivate.
# * If we are still in a virtual environment, stop processing.
# * Check to see if we just entered a virtual environment; if so, activate.
function chpwd() {
    emulate -L zsh
    
    [[ -n $VIRTUAL_ENV ]] && [[ "$VIRTUAL_ENV" != "$PWD" ]] && { parent $VIRTUAL_ENV $PWD || sibling $VIRTUAL_ENV $PWD } && deactivate
    [[ -n $VIRTUAL_ENV ]] && return
    
    [[ -e bin/activate ]] && source bin/activate
    [[ -e src ]] && cd src
}
