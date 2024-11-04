from django import forms
from .models import Profile, Group, Transaction, Campaign

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'major', 'school', 'graduation_year', 'eagle_id', 'user_type']
        widgets = {
            'user_type': forms.Select(attrs={'class': 'form-control'}),
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['campaign', 'user', 'transaction_type']
        widgets = {
            'campaign': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
        }


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['campaign_picture', 'title', 'description', 'start_date', 'end_date', 'individual_points', 'group_points', 'campaign_type']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']