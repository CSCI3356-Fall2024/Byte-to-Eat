from mainApp.models import Profile, Group
from django.contrib.auth.models import User

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "delete test users"

    def handle(self, *args, **kwargs):
        Profile.objects.all().delete()
        Group.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Successfully deleted all test users"))