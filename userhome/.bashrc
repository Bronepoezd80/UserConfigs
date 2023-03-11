# .bashrc
# Jakob Janzen
# 2023-03-11
# jakob.janzen80@gmail.com

# INTERACTIVE SHELL
  # Exit if shell is non-interactive.
[[ $- != *i* ]] && return

# HISTORY CONTROL
export HISTCONTROL=ignoreboth:erasedups
export HISTSIZE=20000
export HISTFILESIZE=10000

# BASH SHELL OPTIONS
shopt -s autocd 2>/dev/null
shopt -s cdspell 2>/dev/null
shopt -s checkwinsize 2>/dev/null
shopt -s direxpand 2>/dev/null
shopt -s dirspell 2>/dev/null
shopt -s dotglob 2>/dev/null
shopt -s histappend 2>/dev/null
shopt -s no_empty_cmd_completion 2>/dev/null
shopt -s nocaseglob 2>/dev/null
shopt -u mailwarn

# WINDOWS TITLE OF X TERMINALS
case $TERM in
  [aEkx]term*|rxvt*|gnome*|konsole*|interix|tmux*) PS1='\[\033]0;\u@\h:\w\007\]';;
  screen*) PS1='\[\033k\u@\h:\w\033\\\]';;
  *) unset PS1;;
esac

# PS1 COLORS
___use_color=false
if type -P dircolors >/dev/null; then
  LS_COLORS=
  if [[ -f ~/.dir_colors ]]; then
    eval "$(dircolors -b ~/.dir_colors)"
  elif [[ -f /etc/$DIR_COLORS ]]; then
    eval "$(dircolors -b /etc/DIR_COLORS)"
  else
    eval "$(dircolors -b)"
  fi
  # Evaluate colors for ls.
  [[ -n ${LS_COLORS:+set} ]] && ___use_color=true || unset LS_COLORS
else
  case $TERM in
  [aEkx]term*|rxvt*|gnome*|konsole*|screen|tmux|cons25|*color) ___use_color=true ;;
  esac
fi

# OTHER COLORS
if $___use_color; then
  [[ $EUID == 0 ]] && \
    PS1+='\[\033[01;31m\]\h\[\033[01;34m\] \w \$\[\033[00m\] ' || \
    PS1+='\[\033[01;32m\]\u@\h\[\033[01;34m\] \w \$\[\033[00m\] '
  alias ls='ls --color=auto'
  alias grep='grep --colour=auto '
  alias diff='diff --color=auto '
  alias ip='ip -color=auto ' 
  # LESS
  export LESS='-R --use-color -Dd+r$Du+b'
  # MANPAGER
  export MANPAGER="less -R --use-color -Dd+r -Du+b"
  # GCC
  export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'
else
  PS1+='\u@\h \w \$ '
fi

# SOURCE ALL SYSTEM BASHRC FILES
for ___sh in /etc/bash/bashrc.d/*; do
  [[ -r $___sh ]] && source $___sh
done

export EDITOR=
if [[ -n $(which nvim) ]]; then
  EDITOR=$(command -v nvim)
elif [[ -n $(which vim) ]]; then
  EDITOR=$(command -v vim)
elif [[ -n $(which nano) ]]; then
  EDITOR=$(command -v nano)
fi
export VISUAL=$EDITOR
alias edit='$EDITOR '

# CLEAN ENVIRONMENT
unset ___use_color ___sh

