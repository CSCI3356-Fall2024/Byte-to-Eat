#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files

python manage.py makemigrations
python manage.py migrate

python manage.py delete_all_campaigns
python manage.py create_test_campaigns

python manage.py collectstatic --no-input


cd EagleEats