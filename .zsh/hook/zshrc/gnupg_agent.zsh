# Alice's over-engineered z-shell configuration.
# GPG/GPG2 settings.

[[ ! -e $HOME/.gnupg/S.gpg-agent ]] && return

export GPG_AGENT_INFO=$HOME/.gnupg/S.gpg-agent:$UID:1
