# Alice's over-engineered z-shell configuration, released in the public domain.
# Oh My Zsh configuration.

ZSH=$ZDOTDIR/oh-my-zsh
ZSH_THEME="alice"
ZSH_CUSTOM=$ZDOTDIR/custom
DISABLE_AUTO_UPDATE=true

ZSH_HIGHLIGHT_HIGHLIGHTERS=(main brackets pattern)

plugins=(git mercurial svn python history-substring-search zsh-syntax-highlighting)

source $ZSH/oh-my-zsh.sh

ZSH_HIGHLIGHT_STYLES[default]=none
ZSH_HIGHLIGHT_STYLES[unknown-token]=fg=214
ZSH_HIGHLIGHT_STYLES[reserved-word]=fg=186,bold
ZSH_HIGHLIGHT_STYLES[alias]=fg=142
ZSH_HIGHLIGHT_STYLES[builtin]=fg=186
ZSH_HIGHLIGHT_STYLES[function]=fg=172
ZSH_HIGHLIGHT_STYLES[command]=fg=white
ZSH_HIGHLIGHT_STYLES[precommand]=fg=186,underline
ZSH_HIGHLIGHT_STYLES[commandseparator]=fg=181
ZSH_HIGHLIGHT_STYLES[hashed-command]=fg=green
ZSH_HIGHLIGHT_STYLES[path]=fg=225
ZSH_HIGHLIGHT_STYLES[globbing]=fg=213
ZSH_HIGHLIGHT_STYLES[history-expansion]=fg=blue
ZSH_HIGHLIGHT_STYLES[single-hyphen-option]=fg=magenta,bold
ZSH_HIGHLIGHT_STYLES[double-hyphen-option]=fg=magenta
ZSH_HIGHLIGHT_STYLES[back-quoted-argument]=fg=141
ZSH_HIGHLIGHT_STYLES[single-quoted-argument]=fg=139
ZSH_HIGHLIGHT_STYLES[double-quoted-argument]=fg=137
ZSH_HIGHLIGHT_STYLES[dollar-double-quoted-argument]=fg=cyan
ZSH_HIGHLIGHT_STYLES[back-double-quoted-argument]=fg=cyan
ZSH_HIGHLIGHT_STYLES[assign]=fg=white,bold

ZSH_HIGHLIGHT_PATTERNS+=('rm -rf' 'fg=white,bold,bg=red')
ZSH_HIGHLIGHT_PATTERNS+=('sudo su' ',fg=white,bold,bg=red')

ZSH_HIGHLIGHT_STYLES[bracket-error]='fg=199'
ZSH_HIGHLIGHT_STYLES[cursor-matchingbracket]='underline,fg=bold'

ZSH_HIGHLIGHT_STYLES[bracket-level-1]='fg=237'
ZSH_HIGHLIGHT_STYLES[bracket-level-2]='fg=239'
ZSH_HIGHLIGHT_STYLES[bracket-level-3]='fg=241'
ZSH_HIGHLIGHT_STYLES[bracket-level-4]='fg=243'
ZSH_HIGHLIGHT_STYLES[bracket-level-5]='fg=245'
ZSH_HIGHLIGHT_STYLES[bracket-level-6]='fg=247'
ZSH_HIGHLIGHT_STYLES[bracket-level-7]='fg=249'
ZSH_HIGHLIGHT_STYLES[bracket-level-8]='fg=251'
ZSH_HIGHLIGHT_STYLES[bracket-level-9]='fg=253'
ZSH_HIGHLIGHT_STYLES[bracket-level-10]='fg=255'
