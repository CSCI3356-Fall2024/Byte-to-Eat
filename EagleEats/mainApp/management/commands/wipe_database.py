from django.db import connection
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "wipe database"

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("DROP SCHEMA public CASCADE;")
            cursor.execute("CREATE SCHEMA public;")