#!/usr/bin/env bash
set -e
set -x
set -u

set -Eeuox pipefail

echo "Setting up autocompletion "
echo ". /etc/bash_completion" >> /etc/bash.bashrc
echo "Done."

