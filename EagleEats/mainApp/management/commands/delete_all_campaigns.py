from django.core.management.base import BaseCommand
from mainApp.models import Campaign

class Command(BaseCommand):
    help = 'Deletes all entries in the Campaign table'

    def handle(self, *args, **kwargs):
        Campaign.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all campaigns'))
