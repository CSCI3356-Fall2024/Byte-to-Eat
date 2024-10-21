from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from mainApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('post-login/', views.post_login_redirect, name='post_login_redirect'),
    path('login/', views.login, name='login'),  # Use Django's built-in LoginView for login and logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path("", views.home, name='home'),
    path("profile/", views.profile, name='profile'),
]