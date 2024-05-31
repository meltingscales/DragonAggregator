#!/usr/bin/env bash
set -euxo pipefail

echo "Make sure poetry exists..."

which poetry || python -m pip install poetry

poetry install