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
    path("home/", views.home, name='home'),
    path("rewards/", views.rewards, name='rewards'),
    path("actions/", views.actions, name='actions'),
    path("campaigns/", views.campaigns, name='campaigns'),
    path('create_group/', views.create_group, name='create_group'),
    path('group/<int:group_id>/invite/', views.invite_to_group, name='invite_to_group'),
    path('groups/', views.groups, name='groups'),
    path('invitation/<int:invitation_id>/accept/', views.accept_invitation, name='accept_invitation'),
    path('invitation/<int:invitation_id>/decline/', views.decline_invitation, name='decline_invitation'),
    path('group/<int:group_id>/leave/', views.leave_group, name='leave_group'),
    path('group/<int:group_id>/delete/', views.delete_group, name='delete_group'),
    path('edit-campaign/<str:campaign_id>/', views.edit_campaign, name='edit_campaign'),
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)