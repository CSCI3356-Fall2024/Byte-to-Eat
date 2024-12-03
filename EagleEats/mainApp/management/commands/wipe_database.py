from mainApp.models import Profile, Group, Campaign
from django.contrib.auth.models import User
from django.db import connection
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "wipe database"

    def handle(self, *args, **kwargs):
        Profile.objects.all().delete()
        Group.objects.all().delete()
        User.objects.all().delete()
        Campaign.objects.all().delete()


        with connection.cursor() as cursor:
            cursor.execute("DROP SCHEMA public CASCADE;")
            cursor.execute("CREATE SCHEMA public;")
        self.stdout.write(self.style.SUCCESS("Successfully wiped database"))