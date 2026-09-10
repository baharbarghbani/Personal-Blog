#!/usr/bin/env bash
set -o errexit

# Liara exposes application environment variables in the pre-start phase.
python manage.py migrate --no-input
python manage.py collectstatic --no-input
