#!/usr/bin/env bash
set -euo pipefail

SELF=$(readlink -f "${BASH_SOURCE[0]}")
DIR=${SELF%/*/*}

function lint()
{
  cmd=(pylint "$1")
  echo "${cmd[*]@Q}"
  "${cmd[@]}" || true
  echo
}

cd -- "$DIR"
if [[ ! -e ./venv ]]
then
  ./scripts/install_in_venv.sh
fi
source ./venv/bin/activate
pip install -U pylint

lint src
lint test
