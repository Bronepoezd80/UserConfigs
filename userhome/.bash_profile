#!/bin/bash
#
# Jakob Janzen
# 2022-12-19
# jakob.janzen80@gmail.com
#


# MAIN CONFIGURATION
___bashrc="${HOME}/.bashrc"
if [[ -n "${BASH_VERSION}" ]]
then
  if [[ -f ${___bashrc} ]]
  then
    source ${___bashrc}
  fi
fi
unset ${___bashrc}


# USER HOME BINARY PATH
___homebin="${HOME}/bin"
if [[ -d ${___homebin} ]]
then
  PATH="${___homebin}:${PATH}"
fi
unset ${___homebin}


# USER HOME LOCAL BINARY PATH
___localbin="${HOME}/.local/bin"
if [[ ! -d ${___localbin} ]]
then
  mkdir -p ${___localbin}
fi
PATH="${___localbin}:${PATH}"
unset ${___localbin}


# PYTHONRC
export PYTHONSTARTUP=${HOME}/.pythonrc

