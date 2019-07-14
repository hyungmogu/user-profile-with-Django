from django import forms

from . import models


class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(input_formats=[
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%m/%d/%y'
    ])

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
        # get cleaned data
        data = self.cleaned_data

        # check and see if it satiesfies the validation criteria
        # 1. date of birth is in one of the three formars: YYYY-MM-DD, MM/DD/YYYY, or MM/DD/YY

        # 2. email address (both confirm email)
        # 3. email adress and confirm email match