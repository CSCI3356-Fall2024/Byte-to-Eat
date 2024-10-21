from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'major', 'school', 'graduation_year', 'eagle_id', 'user_type', 'group_id']
