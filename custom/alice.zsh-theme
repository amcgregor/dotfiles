# Configurable parameters are here.

# NOTE: Removal of local keyword to prevent namespace issues discovered
# when refactoring into this repo.  Previously, local worked.  Now if
# these vars are local the prompt evaluates them to "".  O_o


local rootsymbol='#'
local usersymbol='$'
gitsymbol='±'
hgsymbol='☿'
svnsymbol='⨰'
local nonzeroprefix=''
local nonzerosuffix=' ¬'


local vcs_color="%{$fg_bold[yellow]%}"
local vcs_dirty='⚑'
local vcs_clean='⚐'

local vcs_added=''
local vcs_modified=''
local vcs_deleted=''
local vcs_renamed=''
local vcs_unmerged=''
local vcs_untracked=''

# Do not modify below this line.
return_code="%(?..%{$fg_bold[red]%}${nonzeroprefix}%?${nonzerosuffix}%{$reset_color%})"

if [ $UID -eq 0 ]; then
    user="%{$fg_bold[red]%}%m%{$reset_color%}"
    symbol=$rootsymbol
else
    user="%{$fg_bold[green]%}%n@%m%{$reset_color%}"
    symbol=$usersymbol
fi

function rsymbol {
    git branch >/dev/null 2>/dev/null && echo $gitsymbol && return
    hg root >/dev/null 2>/dev/null && echo $hgsymbol && return
    [ -d .svn ] && echo $svnsymbol && return
    echo $symbol
}

function venv {
    [ $VIRTUAL_ENV ] || return
    echo "  %{$fg_bold[cyan]%}$(basename ${VIRTUAL_ENV} | tr '[A-Z]' '[a-z]')%{$reset_color%}"
}

function apwd {
    if [ $VIRTUAL_ENV ]; then
        echo "${PWD/#$VIRTUAL_ENV/☇}"
    else
        echo "${PWD/#$HOME/~}"
    fi
}

function getla {
    if [[ "$VENDOR" == "apple" ]]; then
        uptime | cut -d ":" -f 4 | cut -d ' ' -f 2
        return
    fi
    cat /proc/loadavg | cut -d " " -f 1
}

ZSH_THEME_GIT_PROMPT_PREFIX=" ${vcs_color}‹"
ZSH_THEME_GIT_PROMPT_SUFFIX=""
ZSH_THEME_GIT_PROMPT_DIRTY="› ${vcs_dirty}"
ZSH_THEME_GIT_PROMPT_CLEAN="› ${vcs_clean}"

ZSH_THEME_SVN_PROMPT_PREFIX=" ${vcs_color}‹"
ZSH_THEME_SVN_PROMPT_SUFFIX=""
ZSH_THEME_REPO_NAME_COLOR=""
ZSH_THEME_SVN_PROMPT_DIRTY="› ${vcs_dirty}"
ZSH_THEME_SVN_PROMPT_CLEAN="› ${vcs_clean}"

setopt PROMPT_SUBST
PROMPT='$user %{$fg_bold[blue]%}$(apwd) $(rsymbol) %{$reset_color%}'
RPS1='${return_code}$(git_prompt_info)$(svn_prompt_info)%{$reset_color%}$(venv)  %{$fg_bold[black]%}$(getla)%{$reset_color%}'

export VIRTUAL_ENV_DISABLE_PROMPT=1
