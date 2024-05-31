#!/usr/bin/env bash
set -euxo pipefail

echo "Make sure poetry exists..."

which poetry
# if exit code is nonzero, it is not a command.
if [ "$?" -eq "1" ]; then
  python -m pip install poetry
fi

poetry install