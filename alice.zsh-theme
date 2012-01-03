# An oh-my-zsh theme with support for git, subversion, mercurial, and virtualenv.
# Looks like: http://cl.ly/1Y2q2j00190n3L373A37

# Configurable parameters are here.

local rootsymbol='#'
local usersymbol='$'
local gitsymbol='±'
local hgsymbol='☿'
local svnsymbol='⨰'
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

local return_code="%(?..%{$fg_bold[red]%}${nonzeroprefix}%?${nonzerosuffix}%{$reset_color%})"

if [ $UID -eq 0 ]; then
    local user="%{$fg_bold[red]%}%m%{$reset_color%}"
    local symbol=$rootsymbol
else
    local user="%{$fg_bold[green]%}%n@%m%{$reset_color%}"
    local symbol=$usersymbol
fi

function rsymbol {
    git branch >/dev/null 2>/dev/null && echo $gitsymbol && return
    hg root >/dev/null 2>/dev/null && echo $hgsymbol && return
    [ -d .svn ] && echo $svnsymbol && return
    echo $symbol
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

PROMPT='${user} %{$fg_bold[blue]%}${PWD/#$HOME/~} $(rsymbol) %{$reset_color%}'
RPS1='${return_code}$(git_prompt_info)$(svn_prompt_info)%{$reset_color%}'
