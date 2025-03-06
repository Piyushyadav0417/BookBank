from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileEditForm, self).__init__(*args, **kwargs)

        # Pre-fill first_name and last_name from User model
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
