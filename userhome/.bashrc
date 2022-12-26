# /etc/bash/bashrc
#
# Jakob Janzen
# 2022-12-19
# jakob.janzen80@gmail.com
#


# INTERACTIVE SHELL
if [[ $- != *i* ]]
then
  # Exit if shell is non-interactive.
  return
fi


# HISTORY CONTROL
export HISTCONTROL=ignoreboth:erasedups
export HISTSIZE=20000
export HISTFILESIZE=10000


# BASH SHELL OPTIONS
#
# If set, a command name that is the name of a directory is executed as if it were
# the argument to the cd command. This option is only used by interactive shells.
shopt -s autocd 2>/dev/null
# If  set,  minor errors in the spelling of a directory component in a cd command
# will be corrected. The errors checked for are transposed characters, a missing
# character, and one character too many. If a correction is found, the corrected
# filename is printed, and the command proceeds. This option is only used by
# interactive shells.
shopt -s cdspell 2>/dev/null
# If set, bash checks the window size after each external (non-builtin) command
# and, if necessary, updates the values of LINES and COLUMNS. This option is
# enabled by default.
shopt -s checkwinsize 2>/dev/null
# If set, bash replaces directory names with the results of word expansion when
# performing filename completion. This changes the contents of the readline editing
# buffer. If not set, bash attempts to preserve what the user typed.
shopt -s direxpand 2>/dev/null
# If set, bash replaces directory names with the results of word expansion when
# performing filename completion. This changes the contents of the readline editing
# buffer. If not set, bash attempts to preserve what the user typed.
shopt -s dirspell 2>/dev/null
# If set, bash includes filenames beginning with a `.' in the results of pathname
# expansion. The filenames ``.'' and ``..'' must always be matched explicitly, even
# if dotglob is set.
shopt -s dotglob 2>/dev/null
# If set, the history list is appended to the file named by the value of the HISTFILE
# variable when the shell exits, rather than overwriting the file.
shopt -s histappend 2>/dev/null
# If set, and readline is being used, bash will not attempt to search the PATH
# for possible completions when completion is attempted on an empty line.
shopt -s no_empty_cmd_completion 2>/dev/null
# If set, bash matches filenames in a case-insensitive fashion when performing
# pathname expansion (see Pathname Expansion above).
shopt -s nocaseglob 2>/dev/null


# WINDOWS TITLE OF X TERMINALS
case ${TERM} in
  [aEkx]term*|rxvt*|gnome*|konsole*|interix|tmux*)
    PS1='\[\033]0;\u@\h:\w\007\]'
    ;;
  screen*)
    PS1='\[\033k\u@\h:\w\033\\\]'
    ;;
  *)
    unset PS1
    ;;
esac


# PS1 COLORS
___use_color=false
if type -P dircolors >/dev/null
then
  # Enable colors for ls.
  LS_COLORS=
  if [[ -f ~/.dir_colors ]]
  then
    eval "$(dircolors -b ~/.dir_colors)"
  elif [[ -f /etc/DIR_COLORS ]]
  then
    eval "$(dircolors -b /etc/DIR_COLORS)"
  else
    eval "$(dircolors -b)"
  fi
  # Evaluate colors for ls.
  if [[ -n ${LS_COLORS:+set} ]]
  then
    ___use_color=true
  else
    # Delete if empty since it is not needed anymore.
    unset LS_COLORS
  fi
else
  # Ensure dircolors for different terminals.
  case ${TERM} in
  [aEkx]term*|rxvt*|gnome*|konsole*|screen|tmux|cons25|*color) ___use_color=true ;;
  esac
fi


# OTHER COLORS
if ${___use_color}
then
  if [[ ${EUID} == 0 ]]
  then
    PS1+='\[\033[01;31m\]\h\[\033[01;34m\] \w \$\[\033[00m\] '
  else
    PS1+='\[\033[01;32m\]\u@\h\[\033[01;34m\] \w \$\[\033[00m\] '
  fi
  #BSD#@export CLICOLOR=1
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
  # Show root@ if no colors.
  PS1+='\u@\h \w \$ '
fi


# SOURCE ALL SYSTEM BASHRC FILES
for ___sh in /etc/bash/bashrc.d/*
do
  [[ -r ${___sh} ]] && source "${___sh}"
done


# CLEAN ENVIRONMENT
unset ___use_color ___sh

