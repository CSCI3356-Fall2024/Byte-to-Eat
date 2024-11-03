from django import forms
from .models import Profile, Group

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'major', 'school', 'graduation_year', 'eagle_id', 'user_type']
        widgets = {
            'user_type': forms.Select(attrs={'class': 'form-control'}),
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']