from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile, Campaign, Transaction, Group, GroupMembership, GroupInvitation
from django.shortcuts import redirect
from .forms import ProfileForm
from django.utils import timezone
from .forms import TransactionForm, CampaignForm 
from .forms import ProfileForm, GroupForm
from django.contrib.auth.models import User 

# Create your views here.
def login(request):
    return render(request, 'login.html')

@login_required
def post_login_redirect(request):
    if request.session.get('is_first_login', False):
        return redirect('profile')
    else:
        return redirect('/')


@login_required
def home(request):
    profile = request.user.profile
    users = Profile.objects.all().filter(user_type="student").order_by('-lifetime_points')[:50]
    groups = Group.objects.all().order_by('-points')[:50]
    return render(request, 'home.html', {'profile': profile, "users": users, "groups": groups})

@login_required
def profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/')  # Redirect to the homepage after updating the profile
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form, 'profile': profile})

@login_required
def actions(request):
    profile = request.user.profile
    today = timezone.now()
    
    # Get active actions/challenges
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
    
    # Get available rewards
    available_rewards = Campaign.objects.filter(
        campaign_type='redeem',
        start_date__lte=today,
        end_date__gte=today
    ).order_by('-start_date')

    context = {
        'profile': profile,
        'available_rewards': available_rewards,
    }
    return render(request, 'rewards.html', context)

@login_required
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
    }
    return render(request, 'campaign.html', context)


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
    return render(request, 'create_group.html', {'form': form})


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
    return render(request, 'groups.html', {'user_group': user_group, 'invitations': invitations, 'profile': profile, 'is_leader': is_leader})