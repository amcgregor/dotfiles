# Alice's over-engineered z-shell configuration, released in the public domain.
# Fancy suffix aliases.  Example: google.com, *.png

# Not suffix aliases, but grouped with the URL handlers below.
alias http://='open http://'
alias https://='open https://'
alias ftp://='open ftp://'
alias sftp://='open sftp://'
alias irc://='open irc://'

# URL handlers.
alias -s com='noglob url'
alias -s org='noglob url'
alias -s net='noglob url'
alias -s ca='noglob url'
alias -s edu='noglob url'
alias -s local='noglob url'
alias -s site='noglob url'
alias -s html='open'

# Compression handlers.  We assume tarballs, not naked compressed files.
alias -s bz2='tar -xjvf'
alias -s gz='tar -xzvf'
alias -s xz='tar -xJvf'

# Image formats.
alias -s gif='open'
alias -s jpg='open'
alias -s jpeg='open'
alias -s png='open'
