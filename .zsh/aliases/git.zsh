# Alice's over-engineered z-shell configuration, released in the public domain.
# Aliases related to the Git SCM system.
# See also my '.gitconfig' in the 'dotfiles' branch for targeted aliases and default arguments.

alias add='git add'
alias br='git branch'
alias ci='noglob git commit'
alias clone='git clone'
alias co='git checkout'
alias gd='git diff'
alias gds='git diff --stat'
alias gf='git fetch'
alias grb='git rebase'
alias grbc='git rebase --continue'
alias grh='git reset --hard'
alias gs='git status -s'
alias pull='git pull'
alias push='git push'
alias st='git status'
alias stash='git stash'
alias tag='git tag'
alias wtf='git wtf'

# Informational aliases.
alias gbranch='git name-rev --name-only HEAD'
alias gcurrent='git log -1 --oneline'
alias gfiles='git ls-tree --name-only -r $(git name-rev --name-only HEAD)'
alias gours='git ls-files --unmerged | cut -f2 | uniq | xargs git checkout --ours'
alias gstage='git diff-index --cached --name-only HEAD'
alias gtheirs='git ls-files --unmerged | cut -f2 | uniq | xargs git checkout --theirs'
alias gtree='git log --graph --all --pretty=format:"%Cred%h%Creset - %Cgreen(%cr)%Creset %s%C(yellow)%d%Creset" --abbrev-commit --date=relative'

function gstats() {
    git log --author="$0" --pretty=tformat: --numstat | grep -v $1 | gawk '{ add += $1 ; subs += $2 ; loc += $1 - $2 } END { printf "added lines: %s removed lines: %s total lines: %s\n",add,subs,loc }' -
}

function gbt() {
    echo > /tmp/gbt
    
    branch="$(git symbolic-ref -q HEAD | sed -e 's|^refs/heads/||')"
    IFS=$'\n' branches=($(git for-each-ref --sort=-committerdate refs/heads/ --format='%(refname:short)[0m|%(objectname:short)|%(contents:subject)|%(authorname), %(committerdate:relative)'))
    
    for b in ${branches[*]}; do
        if [ "$branch" ] && [ "$(echo $b | grep $branch)" ]; then
            echo '|* '"[32m$b" >> /tmp/gbt
        else
            echo '|  '"[29m$b" >> /tmp/gbt
        fi
    done
    
    IFS=$'\n' branches=($(git for-each-ref --sort=-committerdate refs/remotes/ --format='[31mremotes/%(refname:short)[0m|%(objectname:short)|%(contents:subject)|%(authorname), %(committerdate:relative)'))
    
    for b in ${branches[*]}; do
        echo '|  '"$b" >> /tmp/gbt
    done
    
    cat /tmp/gbt | column -t -s "|"
}

function gum() {
    local unmerged unmerged_full stat
    unmerged=${(j:\|:)$(git ls-files --unmerged | cut -f 2 | uniq)}
    
    if [ "$unmerged" ]; then
        IFS=$'\n' unmerged_full=($(git status --short | grep --color=never $unmerged))
    
        # this is all a bit overly complicated, just to get some nice colors ;_;
        for f in $unmerged_full; do
            echo -e "\e[0;31m${f% *}\e[m ${f#* }"
        done
    fi
}