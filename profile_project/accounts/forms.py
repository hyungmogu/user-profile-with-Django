import re

from django import forms
from django.core.validators import MinLengthValidator
from django.contrib.auth.password_validation import (
    validate_password,
    UserAttributeSimilarityValidator,
    MinimumLengthValidator
)

from . import models


# Custom Validators
def contains_combination_upper_lower(value):
    if not re.search(r'[a-z]+', value) or not re.search(r'[A-Z]+', value):
        return False
    return True


def contains_numerical_digits(value):
    if not re.search(r'[0-9]+', value):
        return False

    return True


def contains_special_characters(value):
    if not re.search(r'[^a-zA-Z0-9]+', value):
        return False

    return True

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        current_pw = self.cleaned_data.get('current_password', '')
        new_pw = self.cleaned_data.get('new_password', '')
        confirm_pw = self.cleaned_data.get('confirm_password', '')

        # if current password is not correct, then raise validation error
        if not current_pw or not self.user.check_password(current_pw):
            raise forms.ValidationError(
                'Entered password is incorrect'
            )

        validate_password(new_pw, user=self.user)

        # if new password doesn't have combination of lower and uppercase
        # letters, then raise error
        if not contains_combination_upper_lower(new_pw):
            raise forms.ValidationError(
                'Must contain combination of upper and '
                'lowercase letters')

        # if new password doesn't have numerical digits, then raise error
        if not contains_numerical_digits(new_pw):
            raise forms.ValidationError('Must contain numerical digits')

        # if new password doesn't contain special characters, then raise error
        if not contains_special_characters(new_pw):
            raise forms.ValidationError(
                'Must contain one or more special '
                'characters')

        # if current password and the new password are the same, raise error
        if current_pw == new_pw:
            raise forms.ValidationError(
                'New password must not be the same as old'
            )


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
