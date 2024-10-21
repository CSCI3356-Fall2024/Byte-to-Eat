from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile
from .forms import ProfileForm
import requests

api_link = "https://www.googleapis.com/oauth2/v1/userinfo?alt=json"

# Create your views here.
def login(request):
    try:
        # Make a GET request to the API endpoint using requests.get()
        header = {'Authorization': 'Bearer ' + request.user.social_auth.get().extra_data['access_token']}
        response = requests.get(api_link, headers=header)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            posts = response.json()
            print(posts)
        else:
            print('Error:', response.status_code)
    except requests.exceptions.RequestException as e:
  
        # Handle any network-related errors or exceptions
        print('Error:', e)



    return render(request, 'login.html')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/')  # Redirect to the homepage after updating the profile
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form})