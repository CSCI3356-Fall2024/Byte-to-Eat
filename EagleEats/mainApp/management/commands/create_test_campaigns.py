from django.core.management.base import BaseCommand
from datetime import datetime, timezone
from mainApp.models import Campaign

class Command(BaseCommand):
    help = 'Create test campaigns with images'

    def handle(self, *args, **kwargs):
        # Define campaign data
        campaign_data = [
            {"title": "Cupcakes", "description": "Redeem for free cupcakes", "campaign_type": "redeem", "points": 10, "image": "campaign_pictures/cupcakes.png"},
            {"title": "Sushi", "description": "Redeem for a sushi meal", "campaign_type": "redeem", "points": 15, "image": "campaign_pictures/sushi.png"},
            {"title": "Chicken Wing", "description": "Redeem for free chicken wings", "campaign_type": "redeem", "points": 20, "image": "campaign_pictures/chicken_wing.png"},
            {"title": "Gourd Event - Free Coffee", "description": "Redeem for a free coffee at the Gourd Event", "campaign_type": "redeem", "points": 5, "image": "campaign_pictures/gourd_event.png"},
            {"title": "Chef Mike’s Event", "description": "Attend Chef Mike’s green eating event", "campaign_type": "action", "points": 10, "image": "campaign_pictures/chef.png"},
            {"title": "Farmers Market", "description": "Participate in the Farmers Market event", "campaign_type": "action", "points": 15, "image": "campaign_pictures/farmers_market.png"},
            {"title": "Green2Go", "description": "Use a Green 2 Go box", "campaign_type": "action", "points": 10, "image": "campaign_pictures/green2go.png"},
            {"title": "Green2Go Event", "description": "Attend the Green2Go care and usage event", "campaign_type": "action", "points": 20, "image": "campaign_pictures/green2go_event.png"},
        ]

        # Set date range for all campaigns
        start_date = datetime(2024, 8, 1, 0, 0, 0, tzinfo=timezone.utc)
        end_date = datetime(2025, 1, 1, 23, 59, 59, tzinfo=timezone.utc)

        # Create each campaign
        for data in campaign_data:
            campaign = Campaign(
                title=data["title"],
                description=data["description"],
                start_date=start_date,
                end_date=end_date,
                individual_points=data["points"],
                group_points=data["points"],  # assuming same points for group points
                campaign_type=data["campaign_type"],
                campaign_picture=data["image"]
            )
            campaign.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully created campaign: {campaign.title}'))
