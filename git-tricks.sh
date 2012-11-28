#!/bin/bash

git name-rev --name-only HEAD # current branch
git ls-tree --name-only -r <branch> # files managed in given branch
git ls-tree --name-only -r $(git name-rev --name-only HEAD) # in current branch
git diff-index --cached --name-only HEAD # staged files
git log -1 --oneline # current revision hash and log line for it.
git cat-file -p <hash> # man git-cat-file for awesomness

# helpful shortcut to git-rm rm'd files and add all (modified) files to the stage
git-stage-all() {
    if [ "`git ls-files -d | wc -l`" -gt "0" ]; then; git rm --quiet `git ls-files -d`; fi
    git add .
}

# Danger Zone™ Majick®: Create new, rootless branch.
git symbolic-ref HEAD refs/heads/new ; rm .git/index ; git clean -fdx

# Git does the work for you when tracking down regressions.
# Bisect needs more love.
git bisect start
git bisect bad
git bisect good <hash>

git stash save "<description>" # little known fact: stashes with names

man git-archive # release awesomeness

# pretty tree view
git log --graph --all --pretty=format:'%Cred%h%Creset - %Cgreen(%cr)%Creset %s%C(yellow)%d%creset' --abbrev-commit --date=relative
git log --oneline --date-order --graph --all --decorate # without dates

# per-user change statistics! modify the grep to isolate the files we calculate stats on
git log --author="SOME NAME HERE" --pretty=tformat: --numstat | grep -v public/javascripts/jquery | gawk '{ add += $1 ; subs += $2 ; loc += $1 - $2 } END { printf "added lines: %s removed lines: %s total lines: %s\n",add,subs,loc }' -

man git-grep # search for the -p option ;)
