#!/usr/bin/env bash
set -euxo pipefail

cp ./.dragonaggregator.example.yaml ./.dragonaggregator.yaml
cat ./.dragonaggregator.yaml

poetry run python -m unittest