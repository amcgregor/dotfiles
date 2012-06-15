# Alice's over-engineered z-shell configuration, released in the public domain.
# 

# Don't export the PS1 variable to prevent naive tampering.
typeset +x PS1

case $TERM in
    *xterm*|*rxvt*)
        # Special function precmd, executed before displaying each prompt.
        function precmd() {
            # Set the terminal title to the current working directory.
            print -Pn "\e]0;%n@%m — %~\a"
        }
        
        # Special function preexec, executed before running each command.
        function preexec () {
            print -Pn "\e]2;${2:q} — %~\a"
        }
esac
