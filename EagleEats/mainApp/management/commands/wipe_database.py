import random
from mainApp.models import Profile, Group, Campaign
from django.contrib.auth.models import User

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "wipe database"

    def handle(self, *args, **kwargs):
        Profile.objects.all().delete()
        Group.objects.all().delete()
        User.objects.all().delete()
        Campaign.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Successfully wiped database"))