#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EagleEats.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()



#turns on server
#python3 manage.py runserver

#creates superuser
#python3 manage.py createsuperuser
#created superuser: username, password: password

#makes migrations-- need to run everytime we make a change to the database models
#python3 manage.py makemigrations
#python3 manage.py migrate




#Custom Commands
#creates 8 test campaigns
#python3 manage.py create_test_campaigns

#deletes all campaigns
#python3 manage.py delete_all_campaigns

#andy's user script
#python3 manage.py create_test_users