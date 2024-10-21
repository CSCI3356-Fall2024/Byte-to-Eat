from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
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
    path("home/", views.home, name='home')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)