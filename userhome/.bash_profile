#!/bin/bash
# Jakob Janzen
# 2023-03-11
# jakob.janzen80@gmail.com

# MAIN CONFIGURATION
___bashrc="${HOME}/.bashrc"
[[ -n $BASH_VERSION ]] && [[ -f $___bashrc ]] && source $___bashrc
unset ___bashrc

# USER HOME BINARY PATH
___homebin=$HOME/bin
[[ -d $___homebin ]] && PATH=$___homebin:${PATH}
unset ___homebin

# USER HOME LOCAL BINARY PATH
___localbin=$HOME/.local/bin
[[ ! -d $___localbin ]] && mkdir -p $___localbin
PATH="$___localbin:$PATH"
unset ___localbin

# PYTHONRC
export PYTHONSTARTUP=$HOME/.pythonrc

