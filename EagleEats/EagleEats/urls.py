from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from mainApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # Use Django's built-in LoginView for login and logout
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path("", views.home, name='home'),
    path("profile/", views.profile, name='profile'),
]