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
    
    #dummy data
    
    users = [
        {"first_name": "Bob", "last_name": "Clark", "points": 31483},
        {"first_name": "Alice", "last_name": "Chen", "points": 30322},
        {"first_name": "Robert", "last_name": "Smith", "points": 29412},
        {"first_name": "Johnny", "last_name": "Block", "points": 28453},
        {"first_name": "Trevor", "last_name": "White", "points": 26432},
        {"first_name": "Erica", "last_name": "Park", "points": 26422},
        {"first_name": "Dorris", "last_name": "Will", "points": 25532},
        {"first_name": "Maria", "last_name": "Stark", "points": 25452},
        {"first_name": "Mary", "last_name": "Huel", "points": 25250},
        {"first_name": "Aisha", "last_name": "Wunsch", "points": 25159},
        {"first_name": "Bernie", "last_name": "Wunsch", "points": 25022},
        {"first_name": "Sedrick", "last_name": "Grady", "points": 24449},
        {"first_name": "Bessie", "last_name": "Hills", "points": 23432},
        {"first_name": "Ebony", "last_name": "Abshire", "points": 22432},
        {"first_name": "Chester", "last_name": "Weissnat", "points": 17232},
        {"first_name": "Ally", "last_name": "Herzog", "points": 15431},
        {"first_name": "Anika", "last_name": "Roberts", "points": 15422},
        {"first_name": "Tessie", "last_name": "White", "points": 12732},
        {"first_name": "Carolanne", "last_name": "Jones", "points": 12435}
    ]
    users = 
    return render(request, 'profile.html', {'form': form, 'profile': profile, 'users': users})

@login_required
def campaign(request):
    return render(request, 'campaign.html', {'campaignModel': campaign})

