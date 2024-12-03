from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile, Campaign, Group, GroupMembership, GroupInvitation
from django.shortcuts import redirect
from .forms import ProfileForm
from django.utils import timezone
from .forms import TransactionForm, CampaignForm, RedeemForm
from .forms import ProfileForm, GroupForm, ProfilePictureForm
from django.contrib.auth.models import User 
from django.http import HttpResponseForbidden
from functools import wraps
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.profile.user_type == 'admin':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to view this page.")
    return _wrapped_view


# Create your views here.
def login(request):
    return render(request, 'login.html')

@login_required
def post_login_redirect(request):
    if request.user.profile.eagle_id is None:
        return redirect('profile')
    else:
        return redirect('/')


@login_required
def home(request):
    profile = request.user.profile
    users = Profile.objects.all().filter(user_type="student").order_by('-lifetime_points')[:50]
    groups = Group.objects.all().order_by('-points')[:50]
    profile.update_rank()
    today = timezone.now()
    
    active_actions = Campaign.objects.filter(
        campaign_type='action',
        start_date__lte=today,
        end_date__gte=today
    ).order_by('-start_date')[:5]

    active_rewards = Campaign.objects.filter(
        campaign_type='redeem',
        start_date__lte=today,
        end_date__gte=today
    ).order_by('-start_date')[:5]

    context = {
        'profile': profile,
        'users': users,
        'groups': groups,
        'active_actions': active_actions,
        'active_rewards': active_rewards,
    }
    return render(request, 'home.html', context)

@login_required
def profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
           
    else:
        form = ProfileForm(instance=profile)
    if profile.user_type == 'admin':
        profile.user.is_staff = True
        profile.user.is_superuser = True
        profile.user.save()
    return render(request, 'profile.html', {'form': form, 'profile': profile})

@login_required
def actions(request):
    profile = request.user.profile
    today = timezone.now()
    
    # Get active challenges
    active_campaigns = Campaign.objects.filter(
        campaign_type='action',
        start_date__lte=today,
        end_date__gte=today
    ).order_by('-start_date')

    context = {
        'profile': profile,
        'active_campaigns': active_campaigns,
    }
    return render(request, 'actions.html', context)

@login_required
def rewards(request):
    profile = request.user.profile
    today = timezone.now()
    
    available_rewards = Campaign.objects.filter(
        campaign_type='redeem',
        start_date__lte=today,
        end_date__gte=today
    ).order_by('-start_date')

    # Get rewards for each point threshold
    rewards_1000 = Campaign.objects.filter(
        campaign_type='redeem',
        individual_points=1000,
        start_date__lte=today,
        end_date__gte=today
    )
    
    rewards_1500 = Campaign.objects.filter(
        campaign_type='redeem',
        individual_points=1500,
        start_date__lte=today,
        end_date__gte=today
    )
    
    rewards_2000 = Campaign.objects.filter(
        campaign_type='redeem',
        individual_points=2000,
        start_date__lte=today,
        end_date__gte=today
    )
    
    rewards_2500 = Campaign.objects.filter(
        campaign_type='redeem',
        individual_points=2500,
        start_date__lte=today,
        end_date__gte=today
    )

    # Calculate plant growth based on user's current points
    max_points = 2500
    current_points = profile.current_points
    growth_percentage = (current_points / max_points) * 100 if current_points <= max_points else 100

    # Instantiate the RedeemForm
    redeem_form = RedeemForm(current_points=current_points)

    if request.method == 'POST':
        redeem_form = RedeemForm(request.POST)
        if redeem_form.is_valid():
            # Save the form and associate it with the logged-in user
            redeem_form.save(user=request.user)
            return redirect('rewards')  # Reload the page to show updated data

    context = {
        'profile': profile,
        'available_rewards': available_rewards,
        'rewards_1000': rewards_1000,
        'rewards_1500': rewards_1500,
        'rewards_2000': rewards_2000,
        'rewards_2500': rewards_2500,
        'growth_percentage': growth_percentage,
        'current_points': current_points,
        'redeem_form': redeem_form
    }
    return render(request, 'rewards.html', context)


@login_required
@admin_required
def campaigns(request):
    profile = request.user.profile

    # Get campaigns based on active/inactive status
    today = timezone.now()
    active_campaigns = Campaign.objects.filter(start_date__lte=today, end_date__gte=today)
    inactive_campaigns = Campaign.objects.filter(end_date__lt=today)

    # Instantiate forms
    transaction_form = TransactionForm()
    campaign_form = CampaignForm()

    # Check if request method is POST to process form submissions
    if request.method == 'POST':
        if 'transaction_form' in request.POST:
            # Handle transaction form submission
            transaction_form = TransactionForm(request.POST)
            if transaction_form.is_valid():
                transaction_form.save()
                return redirect('campaigns')  # Reload the page to show updated data

        elif 'save_campaign' in request.POST:
            # Handle campaign form submission
            campaign_form = CampaignForm(request.POST, request.FILES)
            if campaign_form.is_valid():
                campaign_form.save()
                return redirect('campaigns')  # Reload the page to show the new campaign

    # Render the forms and campaign data
    context = {
        'profile': profile,
        'active_campaigns': active_campaigns,
        'inactive_campaigns': inactive_campaigns,
        'transaction_form': transaction_form,
        'campaign_form': campaign_form,
        'settings': settings,
    }
    return render(request, 'campaign.html', context)

@login_required
@admin_required
def edit_campaign(request, campaign_id):
    campaign = Campaign.objects.get(campaign_id=campaign_id)
    if request.method == 'POST':
        if 'save_changes' in request.POST['action']:
            form = CampaignForm(request.POST, request.FILES, instance=campaign)
            if form.is_valid():
                form.save()
                messages.success(request, 'Campaign updated successfully.')
                return redirect('campaigns')
        
        elif 'delete_campaign' in request.POST['action']:
            campaign.delete()
            messages.success(request, 'Campaign deleted successfully.')
            return redirect('campaigns')

    elif request.method == 'GET':
        campaign_data = {
            'title': campaign.title,
            'description': campaign.description,
            'start_date': campaign.start_date.strftime('%Y-%m-%dT%H:%M'),
            'end_date': campaign.end_date.strftime('%Y-%m-%dT%H:%M'),
            'individual_points': campaign.individual_points,
            'group_points': campaign.group_points,
            'campaign_type': campaign.campaign_type,
            'campaign_id': campaign.campaign_id,
        }
        return JsonResponse(campaign_data)
    form = CampaignForm(instance=campaign)
    return render(request, 'campaign.html', {'campaign_form': form, 'campaign': campaign})


@login_required
@admin_required
def reset_group_challenge(request):
    profiles = Profile.objects.all()
    for profile in profiles:
        profile.completed_action = False
        profile.save()
    if request.method == 'POST':
        for group in Group.objects.all():
            group.challenge_completed = False
            group.save()
    return redirect('campaigns')


@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.leader = request.user
            group.save()
            GroupMembership.objects.create(user=request.user, group=group, is_leader=True)
            # Update the user's profile with the new group
            profile = request.user.profile
            profile.group = group
            profile.save()
            return redirect('groups')
    else:
        form = GroupForm()
    return render(request, 'create_group.html', {'form': form, "profile" : request.user.profile})


@login_required
def invite_to_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        user = get_object_or_404(User, username=username)
        profile = user.profile 
        if profile.group is None and group.can_add_member():
            GroupInvitation.objects.create(group=group, invitee=user, invited_by=request.user)
            return redirect('groups')
        else:
            return render(request, 'group_detail.html', {'group': group, 'error': 'User is already in a group or group member limit reached'})

    return render(request, 'group_detail.html', {'group': group})

@login_required
def accept_invitation(request, invitation_id):
    invitation = get_object_or_404(GroupInvitation, id=invitation_id)
    if invitation.invitee == request.user:
        profile = request.user.profile
        profile.group = invitation.group
        profile.save()
        GroupMembership.objects.create(user=request.user, group=invitation.group)
        invitation.accepted = True
        invitation.save()
    return redirect('groups')

@login_required
def decline_invitation(request, invitation_id):
    invitation = get_object_or_404(GroupInvitation, id=invitation_id)
    if invitation.invitee == request.user:
        invitation.delete()
    return redirect('groups')

@login_required
def leave_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    membership = get_object_or_404(GroupMembership, user=request.user, group=group)
    if membership.is_leader:
        return render(request, 'group_detail.html', {'group': group, 'error': 'Leader cannot leave the group. Please delete the group or assign a new leader first.'})
    else:
        membership.delete()
        profile = request.user.profile
        profile.group = None
        profile.save()
        return redirect('groups')

@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    membership = get_object_or_404(GroupMembership, user=request.user, group=group, is_leader=True)
    if membership:
        group.delete()
        return redirect('groups')
    else:
        return render(request, 'group_detail.html', {'group': group, 'error': 'Only the group leader can delete the group.'})

@login_required
def groups(request):
    profile = request.user.profile
    user_group = profile.group
    invitations = GroupInvitation.objects.filter(invitee=request.user, accepted=False)
    is_leader = GroupMembership.objects.filter(user=request.user, group=user_group, is_leader=True).exists() if user_group else False
    if request.method == 'POST':
        if 'profile_picture' in request.FILES:
            profile_picture_form = ProfilePictureForm(request.POST, request.FILES, instance=user_group)
            if profile_picture_form.is_valid():
                profile_picture_form.save()
                return redirect('groups')
        elif request.POST.get('action') == 'delete' and is_leader:
            user_group.delete()
            user_group = None
        else:
            group_form = GroupForm(request.POST, instance=user_group)
            if group_form.is_valid():
                group_form.save()
                return redirect('groups')
    else:
        group_form = GroupForm(instance=user_group)
        profile_picture_form = ProfilePictureForm(instance=user_group)

    if user_group:
        # Calculate the percentage of completed actions
        total_members = user_group.members.count()
        completed_members = Profile.objects.filter(user__in=user_group.members.all(), completed_action=True).count()
        if total_members > 0:
            completion_percentage = round((completed_members / total_members) * 100)
        else:
            completion_percentage = 0
        remaining_members = total_members - completed_members
    else:
        total_members = 0
        completed_members = 0
        completion_percentage = 0
        remaining_members = 0

    return render(request, 'groups.html', {
        'user_group': user_group,
        'invitations': invitations,
        'profile': profile,
        'is_leader': is_leader,
        'group_form': group_form,
        'profile_picture_form': profile_picture_form,
        'completed_members': completed_members,
        'completion_percentage': completion_percentage,
        'total_members': total_members,
        'remaining_members': remaining_members
    })