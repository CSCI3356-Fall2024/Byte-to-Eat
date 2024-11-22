from django import forms
from .models import Profile, Group, Transaction, Campaign
from django.utils import timezone

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['major'].required = True
        self.fields['graduation_year'].required = True
        self.fields['eagle_id'].required = True
        
    class Meta:
        model = Profile
        fields = ['profile_picture', 'major', 'school', 'graduation_year', 'eagle_id', 'user_type']
        widgets = {
            'user_type': forms.Select(attrs={'class': 'form-control'}),
        }

class RedeemForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['campaign']  # Only include the campaign field
        widgets = {
            'campaign': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        current_points = kwargs.pop('current_points', 0)  # Get current_points from kwargs
        super().__init__(*args, **kwargs)
        today = timezone.now()
        # Filter campaigns to show only active redeem campaigns the user can afford
        self.fields['campaign'].queryset = Campaign.objects.filter(
            campaign_type='redeem',
            start_date__lte=today,
            end_date__gte=today
            #,individual_points__lte=current_points  # Only campaigns within the user's budget
        )

    def save(self, user, commit=True):
        # Create the transaction and associate it with the logged-in user
        instance = super().save(commit=False)
        instance.user = user
        instance.transaction_type = 'redeem'  # Explicitly set transaction type
        if commit:
            instance.save()
        return instance



class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['campaign', 'user']  # Removed 'transaction_type' field
        widgets = {
            'campaign': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter campaigns to show only active ones
        today = timezone.now()
        self.fields['campaign'].queryset = Campaign.objects.filter(start_date__lte=today, end_date__gte=today)

    def save(self, commit=True):
        # Autofill transaction_type based on selected campaign's type
        instance = super().save(commit=False)
        instance.transaction_type = instance.campaign.campaign_type
        if commit:
            instance.save()
        return instance


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['campaign_picture', 'title', 'description', 'start_date', 'end_date', 'individual_points', 'group_points', 'campaign_type']
        readonly_fields = ['campaign_id']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'resize: none;', 'rows': 3}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
        
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['profile_picture']