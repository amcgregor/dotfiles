# Alice's over-engineered z-shell configuration, released in the public domain.
# More complicated function-based helpers.

function pipr() {
    if [ $1 ]; then
        pip install -r $@
    else
        pip install -r requirements.txt
    fi
}

# Print the length of a string.
function len() {
    local x
    x=$*
    echo ${#x}
}

# Helper for iterating over file globs.
function fof() {
    local f
    local files=$1
    
    shift
    local cmd=$@
    
    for f in ${~files}; do
        ${=cmd} $f
    done
}

# I like not having to write a .sh script for this.
function pskill() { 
    local pid
    pid=$(ps -ax | grep $1 | grep -v grep | awk '{ print $1 }')

    [[ "$pid" = "" ]] && return 1

    echo -en "Killing $1 with PID $pid"

    for i in {0..3}; do
        sleep 1
        echo -en "."
    done

    echo -en " "
    kill -9 $=pid
    echo "slaughtered."
}

# Completely reload the shell environment.
function reload() {
    # First, fix any terminal corruption.
    stty sane
    reset
    stty sane
    reset

    # Then reload zsh configuration.
    autoload -U zrecompile

    [ -f ~/.zshrc ] && zrecompile -p ~/.zshrc
    [ -f ~/.zcompdump ] && zrecompile -p ~/.zcompdump
    [ -f ~/.zshrc.zwc.old ] && rm -f ~/.zshrc.zwc.old
    [ -f ~/.zcompdump.zwc.old ] && rm -f ~/.zcompdump.zwc.old

    source ~/.zshrc

    hash -r
}

# Calculate, as best we can, the Xterm-256 colour code for the given float RGB values.
function rgb() {
    local c
    integer c=$[36 * ($1 * 5) + 6 * ($2 * 5) + ($3 * 5) + 16]
    print $c
}

# Calculate, as best we can, the Xterm-256 greyscale gradient value for the given float luminosity.
function grey() {
    local c
    integer c=$[23*$1+232]
    print $c
}

# Generate tables of Xterm-256 colours.
function allcolors() {
    local tmp

    print "ANSI Colours"
    tmp=$(for i in {0..15}; do echo -e "\e[38;05;${i}m${i}"; done | column -x -c 200 -s '')
    print $tmp "\e[m"

    print "\nXterm-256 Colours"
    tmp=$(for i in {16..231}; do echo -e "\e[38;05;${i}m${i}"; done | column -x -c 155 -s '  ')
    print $tmp "\e[m"

    print "\nXterm-256 Greyscale"
    tmp=$(for i in {232..255}; do echo -e "\e[38;05;${i}m${i}"; done | column -x -c 200 -s '  ')
    print $tmp "\e[m"
}


b64decode(){ python -c "import base64, sys; print base64.decodestring(''.join(sys.argv[1:]))" $@ }
b64encode(){ python -c "import base64, sys; print base64.encodestring(''.join(sys.argv[1:]))" $@ }
hexdecode(){ python -c "import sys; print ''.join(chr(int(''.join(i), 16)) for i in zip(*[iter(''.join(sys.argv[1:]))]*2))" $@ }
urlencode(){ python -c "import urllib, sys; print urllib.quote(''.join(sys.argv[1:]))" $@ }
urldecode(){ python -c "import urllib, sys; print urllib.unquote(''.join(sys.argv[1:]))" $@ }
cdsp() {
    local spdir=`python -c 'from distutils.sysconfig import get_python_lib; print get_python_lib()'`
    if [ $1 ]; then
        if [ "$1" = '--location' ]; then
            echo $spdir
        else
            cd $spdir/$1
        fi
    else
        cd $spdir
    fi
}


screen-clean() {
    local -a screens
    screens=( ${(f)"$(screen -ls | grep '(Detached)' | grep -o '[0-9]*.tty[0-9]*')"} )
    for screen in $screens
    do
        screen -X -S $screen kill
    done
}

screen-kill() {
    local -a screens
    screens=( ${(f)"$(screen -ls | grep -o '[0-9]*.tty[0-9]*')"} )
    for screen in $screens
    do
        screen -X -S $screen kill
    done
}

