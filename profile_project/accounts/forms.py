from django import forms

from . import models


class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(input_formats=[
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%m/%d/%y'
    ], error_messages={'invalid': (
            'Date must be one of the following formats '
            '(YYYY-MM-DD, MM/DD/YYYY, MM/DD/YY)'
        )})

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

    def clean(self):
        # get sanitized data
        email = self.cleaned_data['email']
        email_verify = self.cleaned_data['confirm_email']

        # check and see if it satiesfies the validation criteria
        # 1. email adresss and confirm email match
        # 2. both email and confirm email are of correct format
        # [done by EmailField]
        if (email or email_verify) and email != email_verify:
            raise forms.ValidationError((
                    'Please ensure that Confirm Email and '
                    'Email match'
                ))
