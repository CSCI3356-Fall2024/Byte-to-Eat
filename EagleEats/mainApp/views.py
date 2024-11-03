from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, GroupForm
from .models import Group, Profile, GroupInvitation
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
    users = Profile.objects.all().filter(user_type="student").order_by('-lifetime_points')
    return render(request, 'home.html', {'profile': profile, "users": users})

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
def campaign(request):
    profile = request.user.profile
    return render(request, 'campaign.html', {'campaignModel': campaign, 'profile': profile })

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.leader = request.user
            group.save()
            profile = request.user.profile
            profile.group = group
            profile.save()
            return redirect('group_detail', group_id=group.id)
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
            return redirect('group_detail', group_id=group.id)
        else:
            return render(request, 'group_detail.html', {'group': group, 'error': 'User is already in a group or group member limit reached'})

    return render(request, 'group_detail.html', {'group': group})

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'group_detail.html', {'group': group})

@login_required
def accept_invitation(request, invitation_id):
    invitation = get_object_or_404(GroupInvitation, id=invitation_id)
    if invitation.invitee == request.user:
        profile = request.user.profile
        profile.group = invitation.group
        profile.save()
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
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'group_detail.html', {'group': group})

@login_required
def groups(request):
    profile = request.user.profile
    user_group = profile.group
    invitations = GroupInvitation.objects.filter(invitee=request.user, accepted=False)
    return render(request, 'groups.html', {'user_group': user_group, 'invitations': invitations})