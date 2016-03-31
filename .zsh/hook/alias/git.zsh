# Alice's over-engineered z-shell configuration, released in the public domain.
# Aliases related to the Git SCM system.
# See also my '.gitconfig' in the 'dotfiles' branch for targeted aliases and default arguments.

alias br='git branch'
alias ci='noglob git commit'
alias co='git checkout'
alias gd='git diff'
alias gds='git diff --stat'
alias gf='git fetch'
alias gint='git init'
alias grb='git rebase'
alias grbc='git rebase --continue'
alias grh='git reset --hard'
alias gs='git status -s'
alias st='git status'
alias wtf='git wtf'

alias add='git add'
alias clone='git clone'
alias pull='git pull'
alias push='git push'
alias remote='git remote'
alias stash='git stash'

# Informational aliases.
alias gbranch='git name-rev --name-only HEAD'
alias gcurrent='git log -1 --oneline'
alias gfiles='git ls-tree --name-only -r $(git name-rev --name-only HEAD)'
alias gours='git ls-files --unmerged | cut -f2 | uniq | xargs git checkout --ours'
alias gstage='git diff-index --cached --name-only HEAD'
alias gtheirs='git ls-files --unmerged | cut -f2 | uniq | xargs git checkout --theirs'
alias gtree='git log --graph --all --pretty=format:"%Cred%h%Creset - %Cgreen(%cr)%Creset %s%C(yellow)%d%Creset" --abbrev-commit --date=relative'
alias gauthors="git log --format='%aN <%aE>' | sort -u | egrep -v '\+ed'"

