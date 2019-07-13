from django import forms

from . import models


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = [
            'first_name',
            'last_name',
            'date_of_birth',
            'email',
            'confirm_email',
            'short_bio',
            'avatar'
        ]