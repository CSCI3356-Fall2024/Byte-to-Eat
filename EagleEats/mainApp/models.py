from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.utils import timezone


class Group(models.Model):
    name = models.CharField(max_length=40)
    member_limit = models.IntegerField(default=10)
    points = models.IntegerField(default=0) #need to set this up later
    leader = models.ForeignKey(User, related_name= 'led_groups', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def can_add_member(self):
        return self.profile_set.count() < self.member_limit

class Profile(models.Model):
    USER_TYPES = [
        ('student', 'Student'),
        ('mod', 'Moderator'),
        ('admin', 'Admin'),
    ]
    
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.CharField(max_length=100, blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    graduation_year = models.IntegerField(blank=True, null=True)
    eagle_id = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')
    email = models.EmailField(max_length=100, blank=True)
    group_id = models.IntegerField(blank=True, null=True)
    
    # Point-related fields
    lifetime_points = models.IntegerField(default=0)
    current_points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Campaign(models.Model):
    CAMPAIGN_TYPE_CHOICES = [
        ('action', 'Action'),
        ('redeem', 'Redeem')
    ]
    
    campaign_picture = models.ImageField(upload_to='campaign_pictures/', null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    individual_points = models.IntegerField(default=0)
    group_points = models.IntegerField(default=0)
    campaign_type = models.CharField(max_length=10, choices=CAMPAIGN_TYPE_CHOICES)
    campaign_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.title

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=20, unique=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=Campaign.CAMPAIGN_TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.campaign.title} - {self.transaction_type}"

@receiver(post_save, sender=Transaction)
def update_user_points(sender, instance, created, **kwargs):
    if created:
        profile = instance.user.profile
        campaign_points = instance.campaign.individual_points

        if instance.transaction_type == 'action':
            profile.lifetime_points += campaign_points
            profile.current_points += campaign_points
        elif instance.transaction_type == 'redeem':
            profile.current_points -= campaign_points

        profile.save()

# Signals to auto-create Profile on User creation
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        email_domain = instance.email.split('@')[1] if instance.email else None
        school_name = "Boston College" if email_domain == "bc.edu" else email_domain

        Profile.objects.create(
            user=instance,
            email=instance.email,
            school=school_name
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
