from django import forms
from .models import Profile, Group, Transaction, Campaign
from django.utils import timezone

class ProfileForm(forms.ModelForm):
    MAJOR_CHOICES = [
        # Morrisey College of Arts and Sciences
        ('AAD', 'African and African Diaspora Studies'),
        ('APH', 'Applied Physics'),
        ('AH', 'Art History'),
        ('BCH', 'Biochemistry'),
        ('BIO', 'Biology'),
        ('CHM', 'Chemistry'),
        ('CLS', 'Classics'),
        ('COM', 'Communication'),
        ('CS', 'Computer Science'),
        ('ECON', 'Economics'),
        ('ENG', 'English'),
        ('ENVG', 'Environmental Geoscience'),
        ('ENVS', 'Environmental Studies'),
        ('FILM', 'Film Studies'),
        ('FREN', 'French'),
        ('GEO', 'Geological Sciences'),
        ('GER', 'German Studies'),
        ('HISP', 'Hispanic Studies'),
        ('HIST', 'History'),
        ('ENGR', 'Human-Centered Engineering'),
        ('IND', 'Independent'),
        ('IS', 'International Studies'),
        ('ICS', 'Islamic Civilization and Societies'),
        ('ITAL', 'Italian'),
        ('LING', 'Linguistics'),
        ('MATH', 'Mathematics'),
        ('MUS', 'Music'),
        ('NEURO', 'Neuroscience'),
        ('PHIL', 'Philosophy'),
        ('PHYS', 'Physics'),
        ('POLI', 'Political Science'),
        ('PSY', 'Psychology'),
        ('RUS', 'Russian'),
        ('SLAV', 'Slavic Studies'),
        ('SOC', 'Sociology'),
        ('ART', 'Studio Art'),
        ('THEA', 'Theatre'),
        ('THEO', 'Theology'),
        # Lynch School of Education and Human Development
        ('AH', 'American Heritage'),
        ('APHD', 'Applied Psychology and Human Development'),
        ('EDU', 'Elementary Education'),
        ('MATH_CS', 'Mathematics/Computer Science'),
        ('PSA', 'Perspectives on Spanish America'),
        ('SED', 'Secondary Education'),
        ('TES', 'Transformative Educational Studies'),
        # Carroll School of Management
        ('ACCT', 'Accounting'),
        ('AFC', 'Accounting for Finance and Consulting'),
        ('BUS_ANL', 'Business Analytics'),
        ('ENT', 'Entrepreneurship'),
        ('FIN', 'Finance'),
        ('GEN_MGT', 'General Management'),
        ('MGT_LDR', 'Management and Leadership'),
        ('MKT', 'Marketing'),
        ('OPS_MGT', 'Operations Management'),
        # Connell School of Nursing
        ('GPH', 'Global Public Health and the Common Good'),
        ('NURS', 'Nursing'),
        # Woods College of Advancing Studies
        ('ALA', 'Applied Liberal Arts'),
        ('ENG_WC', 'English'),
        ('HIST_WC', 'History'),
        ('IDS', 'Interdisciplinary Studies'),
        ('PHIL_WC', 'Philosophy'),
        ('POLI_WC', 'Political Science'),
        ('SOC_WC', 'Sociology'),
        ('BUS_WC', 'Business'),
        ('CSJ', 'Criminal and Social Justice'),
        ('CYBER', 'Cybersecurity'),
        ('DGC', 'Digital Communications'),
        ('ECON_WC', 'Economics'),
        ('IT', 'Information Technology'),
        ('PSY_WC', 'Psychology'),
        # Messina College
        ('ADS', 'Applied Data Science'),
        ('APHD_M', 'Applied Psychology and Human Development'),
        ('GBUS', 'General Business'),
        ('HS', 'Health Sciences'),
            ]


    second_major = forms.ChoiceField (
        choices=[('', 'Select your major')] + MAJOR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['major'].required = True
        self.fields['graduation_year'].required = True
        self.fields['eagle_id'].required = True
        
    class Meta:
        model = Profile
        fields = ['profile_picture', 'major', 'second_major','school', 'graduation_year', 'eagle_id', 'user_type']
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
            ,individual_points__lte=current_points  # Only campaigns within the user's budget
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