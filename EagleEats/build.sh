#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files

python manage.py wipe_database
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py create_test_users

python manage.py collectstatic --no-input
