from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.utils import timezone
import uuid
from django.conf import settings


class Group(models.Model):
    name = models.CharField(max_length=40)
    member_limit = models.IntegerField(default=10)
    earned_points = models.IntegerField(default=0)
    points = models.IntegerField(default=0) #total points
    group_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    members = models.ManyToManyField(User, related_name='member_list', through='GroupMembership')
    leader = models.ForeignKey(User, related_name='led_groups', on_delete=models.SET_NULL, null=True, blank=True)
    rank = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to='group_pics/', null=True, blank=True, default= 'img/profile.png')
    challenge_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name 

    def can_add_member(self):
        return self.profile_set.count() < self.member_limit

    def update_rank(self):
        self.rank = Group.objects.filter(points__gt=self.points).count() + 1
        self.save()

    def update_points(self):
        total_points = self.earned_points
        for member in self.members.all():
            total_points += member.profile.lifetime_points
        self.points = total_points
        self.save()

class Profile(models.Model):
    USER_TYPES = [
        ('student', 'Student'),
        ('admin', 'Supervisor'),
    ]
    
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.CharField(max_length=100, blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    graduation_year = models.IntegerField(blank=True, null=True)
    eagle_id = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')
    email = models.EmailField(max_length=100, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    rank = models.IntegerField(default=0)
    completed_action = models.BooleanField(default=False)

    # Point-related fields
    lifetime_points = models.IntegerField(default=0)
    current_points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    
    def update_rank(self):
        if self.group:
            self.group.update_rank()
        self.rank = Profile.objects.filter(lifetime_points__gt=self.lifetime_points).count() + 1
        self.save()

class GroupMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_leader = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"


#when to update the group's total points
@receiver(post_save, sender=Profile)
def update_group_points_on_profile_save(sender, instance, **kwargs):
    if instance.group:
        instance.group.update_points()

@receiver(post_save, sender=GroupMembership)
def update_group_points_on_membership_save(sender, instance, **kwargs):
    instance.group.update_points()

@receiver(models.signals.post_delete, sender=GroupMembership)
def update_group_points_on_membership_delete(sender, instance, **kwargs):
    instance.group.update_points()
    


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
            profile.completed_action = True #sets the boolean true for the group challenge
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

class GroupInvitation(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    invitee = models.ForeignKey(User, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(User, related_name='sent_invitations', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Invite to {self.invitee.username} from {self.invited_by.username} for {self.group.name}"

# Automatically generate campaign ID
@receiver(pre_save, sender=Campaign)
def set_campaign_id(sender, instance, **kwargs):
    if not instance.campaign_id:  # Only set ID if it doesn't exist
        last_campaign = Campaign.objects.order_by('-campaign_id').first()
        instance.campaign_id = f'C{int(last_campaign.campaign_id[1:]) + 1 if last_campaign else 1:04d}'

# Automatically generate transaction ID and check campaign status
@receiver(pre_save, sender=Transaction)
def set_transaction_id_and_validate(sender, instance, **kwargs):
    # Set transaction ID
    if not instance.transaction_id:
        last_transaction = Transaction.objects.order_by('-transaction_id').first()
        instance.transaction_id = f'T{int(last_transaction.transaction_id[1:]) + 1 if last_transaction else 1:04d}'
    
    # Validate campaign is active
    today = timezone.now()
    if not (instance.campaign.start_date <= today <= instance.campaign.end_date):
        raise ValueError("Cannot assign transactions to inactive campaigns.")

@receiver(post_save, sender=Transaction)
def handle_transaction(sender, instance, **kwargs):
    user = instance.user
    group = user.member_list.first()  # Assuming a user belongs to one group

    if group:
        check_and_update_group_points(group)


def check_and_update_group_points(group):
   if not group.challenge_completed:
        all_completed = all(member.profile.completed_action for member in group.members.all())
        if all_completed:
           group.earned_points += settings.GROUP_CHALLENGE_POINTS
           group.update_points()  # Update total points
           group.challenge_completed = True
           group.save()