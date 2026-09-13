#!/usr/bin/env bash
set -o errexit

python -m pip install -e ".[dev]"

python manage.py collectstatic --no-input

python manage.py migrate