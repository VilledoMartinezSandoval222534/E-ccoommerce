#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

echo "=== Contenido de staticfiles ==="
ls -lah staticfiles

python manage.py migrate
