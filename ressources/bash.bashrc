#
# /etc/bash.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

PS1='[\u@\h \W]\$ '
PS2='> '
PS3='> '
PS4='+ '

case ${TERM} in
  xterm*|rxvt*|Eterm|aterm|kterm|gnome*)
    PROMPT_COMMAND=${PROMPT_COMMAND:+$PROMPT_COMMAND; }'printf "\033]0;%s@%s:%s\007" "${USER}" "${HOSTNAME%%.*}" "${PWD/#$HOME/~}"'

    ;;
  screen)
    PROMPT_COMMAND=${PROMPT_COMMAND:+$PROMPT_COMMAND; }'printf "\033_%s@%s:%s\033\\" "${USER}" "${HOSTNAME%%.*}" "${PWD/#$HOME/~}"'
    ;;
esac

[ -r /usr/share/bash-completion/bash_completion   ] && . /usr/share/bash-completion/bash_completion

#loadkeys cf

# Aliases
alias ls='ls --color=auto'
alias ll='ls -lhA'
alias la='ls -A'
alias doit='apt-get update && apt-get dist-upgrade && apt-get autoclean && apt-get autoremove'
alias diff='colordiff'
alias grep='grep --color=auto'
alias df='df -h'
alias du='du -c -h'
alias ping='ping -c 3'
alias ..='cd ..'
alias torrent='stty stop undef; stty start undef; screen -r rtd'
alias watchfreq='watch -n 0.3 cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq'

# Active automatiquement le virtualenv du projet Marcus
source /root/marcus/bin/activate
cd /root/marcus
