#!/bin/bash
#
# Jakob Janzen
# jakob.janzen80@gmail.com
# 2023-02-20
#
# Automatically install or remove packages according a list.
#
__THIS_DIR=$(dirname ${0})
__PACKAGES_FILE=${__THIS_DIR}/packages.txt
__ARCH=amd64

echo "======================"
echo "PACKAGES AUTOINSTALLER"
echo "======================"

pkg_install() {
  # 1 - packages
  echo "-------------------------------------------------------------------------------"
  echo "INSTALL PACKAGES - ${1}:"
  sudo apt -y install ${1}
}

pkg_remove() {
  # 1 - packages
  echo "-------------------------------------------------------------------------------"
  echo "REMOVE PACKAGES - ${1}:"
  sudo apt -y remove ${1}
}

#==============================================================================
# MAIN
(
  if [[ -f ${__PACKAGES_FILE} ]]; then
    (
      echo "UPDATE DATABASE"
      sudo apt update 2>/dev/null

      __is_install=0
      __is_remove=0
      while IFS= read -r __line; do
        __packages=$(echo "${__line}" | xargs)

        # Remove comments.
        __packages=$(echo "${__packages}" | cut -d'#' -f1 | xargs)

        # Skip empty lines.
        if [[ -z ${__packages} ]]; then
          continue
        fi

        # Set flag for action.
        if echo "${__packages}" | grep INSTALL >/dev/null 2>&1; then
          __is_install=1
          __is_remove=0
          continue
        elif echo "${__packages}" | grep REMOVE >/dev/null 2>&1; then
          __is_install=0
          __is_remove=1
          continue
        fi

        # Execute actions.
        echo
        if [[ ${__is_install} == 1 ]]; then
          pkg_install "${__packages}"
        elif [[ ${__is_remove} == 1 ]]; then
          pkg_remove "${__packages}"
        fi
      done <"${__PACKAGES_FILE}"
    )
    echo
  fi
)
#==============================================================================
