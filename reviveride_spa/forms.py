from django import forms
from django.contrib.auth.models import User
from .models import Profile

class CombinedProfileForm(forms.Form):
    # Fields from User model
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)

    # Fields from Profile model
    profile_image = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get user object from view
        super().__init__(*args, **kwargs)

        # Pre-fill form fields with current user data
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email
            if hasattr(self.user, 'profile'):
                self.fields['profile_image'].initial = self.user.profile.profile_image

    def save(self):
        # Update User fields
        self.user.first_name = self.cleaned_data.get('first_name', '')
        self.user.last_name = self.cleaned_data.get('last_name', '')
        self.user.email = self.cleaned_data.get('email', '')
        self.user.save()

        # Update Profile image
        profile = self.user.profile
        if self.cleaned_data.get('profile_image'):
            profile.profile_image = self.cleaned_data['profile_image']
        profile.save()
