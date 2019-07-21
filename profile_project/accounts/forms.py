import re

from django import forms
from django.core.validators import MinLengthValidator
from django.contrib.auth.password_validation import (
    validate_password,
    UserAttributeSimilarityValidator,
    MinimumLengthValidator
)

from . import models


def contains_first_or_last_name_or_username(value, user, profile):
    """
    Checks if password contains first last or username

    Args:
        value: user password (strng)

    Returns:
        Boolean
    """

    if profile.first_name.lower() in value.lower():
        return True

    if profile.last_name.lower() in value.lower():
        return True

    if user.username.lower() in value.lower():
        return True

    return False


# Custom Validators
def contains_combination_upper_lower(value):
    """
    Checks if a string contains both uppercase and lowercase letters

    Args:
        value: user password (strng)

    Returns:
        Boolean
    """
    if not re.search(r'[a-z]+', value) or not re.search(r'[A-Z]+', value):
        return False
    return True


def contains_numerical_digits(value):
    """
    Checks if a string contains numerical digits

    Args:
        value: user password (strng)

    Returns:
        Boolean
    """
    if not re.search(r'[0-9]+', value):
        return False

    return True


def contains_special_characters(value):
    """
    Checks if a string contains special characters (non-alphanumerical symbols)

    Args:
        value: user password (strng)

    Returns:
        Boolean
    """
    if not re.search(r'[^a-zA-Z0-9]+', value):
        return False

    return True


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        profile = kwargs.pop('profile')
        self.user = user
        self.profile = profile
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
        Checks if validation for ChangePasswordForm satisfies the following
        criteria
            - Must not be the same as the current password
            - Minimum password length of 14 characters.
            - Must use of both uppercase and lowercase letters
            - Must include of one or more numerical digits
            - Must include of special characters, such as @, #, $
            - Cannot contain the username or parts of thde user’s full name,
            such as his first name

        Args:
            None

        Return:
            None

        Raises:
            Validation Error if any one of the above criteria are not met
        """

        current_pw = self.cleaned_data.get('current_password', '')
        new_pw = self.cleaned_data.get('new_password', '')
        confirm_pw = self.cleaned_data.get('confirm_password', '')

        # if current password is not correct, then raise validation error
        # if new password has length less than 14, then raise validation error
        if len(new_pw) < 14:
            raise forms.ValidationError(
                'Password must be more than 14 characters'
            )

        if not current_pw or not current_pw == self.user.password:
            raise forms.ValidationError(
                'Entered password is incorrect'
            )

        if contains_first_or_last_name_or_username(
                new_pw,
                self.user,
                self.profile):
            raise forms.ValidationError(
                'Entered password must not contain first or last name '
                'nor username')

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
        """
        Checks if validation for ProfileForm satisfies the following criteria
            - Date of birth accepts three formats  YYYY-MM-DD, MM/DD/YYYY, or
            MM/DD/YY (see input_format in date_of_birth)
            - Email validation checks if the email addresses match and is a
            valid format
            - Text field validation checks for characters longer than 10
            characters and ensuring HTML

        Args:
            None

        Return:
            None

        Raises:
            Validation Error if any one of the above criteria are not met
        """

        # get sanitized data
        email = self.cleaned_data['email']
        email_verify = self.cleaned_data['confirm_email']

        if (email or email_verify) and email != email_verify:
            raise forms.ValidationError((
                    'Please ensure that Confirm Email and '
                    'Email match'
                ))
