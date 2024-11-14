from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import ProfileForm

# Create your views here.
def login(request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')


@login_required
def post_login_redirect(request):
    if request.session.get('is_first_login', False):
        return redirect('profile')
    else:
        return redirect('/')


@login_required
def home(request):
    profile = request.user.profile
    return render(request, 'home.html', {'profile': profile})

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

def actions(request):
    profile = request.user.profile
    return render(request, 'actions.html', {'profile': profile})