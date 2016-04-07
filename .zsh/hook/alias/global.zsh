# Alice's over-engineered z-shell configuration, released in the public domain.
# Fancy global aliases.  Example: ls G .pyc W

alias -g L='| less'
alias -g G='| grep'
alias -g T='| tail'
alias -g H='| head'
alias -g W='| wc -l'
alias -g S='| sort'
alias -g US='| sort -u'
alias -g NS='| sort -n'
alias -g RNS='| sort -nr'
alias -g N='&> /dev/null'
alias -g XA='| xargs'
alias -g XAE='| xargs --no-run-if-empty'
