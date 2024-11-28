#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

python manage.py makemigrations
# Apply any outstanding database migrations
python manage.py migrate

python manage.py wipe_database
python manage.py create_test_campaigns
python manage.py create_test_users
python manage.py createsuperuser --username admin --email swe.bte123@gmail.com --noinput

cd EagleEats