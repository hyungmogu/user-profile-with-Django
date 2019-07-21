from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from accounts.models import Profile
from accounts.forms import ProfileForm, ChangePasswordForm


# MODEL TEST
class PasswordFromTest(TestCase):
    def setUp(self):
        # create user
        self.user = User.objects.create(
            password="hello1", username="test")

        # create derivate profile
        self.profile = Profile.objects.create(
            user=self.user,
            first_name="Moe",
            last_name="Gu"
        )

    def test_return_form_invalid_if_current_password_incorrect(self):
        expected = False

        form = ChangePasswordForm(
            data={
                'current_password': 'hello',
                'new_password': 'MoeIs5!2345444555666',
                'confirm_password': 'MoeIs5!2345444555666'},
            user=self.user,
            profile=self.profile)

        result = form.is_valid()

        self.assertEqual(expected, result)

    def test_return_form_invalid_if_contains_first_name(self):
        expected = False

        # change password using the password change form
        form = ChangePasswordForm(
            data={
                'current_password': self.user.password,
                'new_password': 'MoeIs5!2345444555666',
                'confirm_password': 'MoeIs5!2345444555666'},
            user=self.user,
            profile=self.profile)

        result = form.is_valid()

        self.assertEqual(expected, result)

    def test_return_form_invalid_if_contains_last_name(self):
        expected = False

        # change password using the password change form
        form = ChangePasswordForm(
            data={
                'current_password': self.user.password,
                'new_password': 'IsGu5!2345444555666',
                'confirm_password': 'IsGu5!2345444555666'},
            user=self.user,
            profile=self.profile)

        result = form.is_valid()

        self.assertEqual(expected, result)

    def test_return_form_invalid_if_contains_username(self):
        expected = False

        # change password using the password change form
        form = ChangePasswordForm(
            data={
                'current_password': self.user.password,
                'new_password': 'IsTest5!2345444555666',
                'confirm_password': 'IsTest5!2345444555666'},
            user=self.user,
            profile=self.profile)

        result = form.is_valid()

        self.assertEqual(expected, result)

    def test_return_form_valid_if_contains_username(self):
        expected = True

        # change password using the password change form
        form = ChangePasswordForm(
            data={
                'current_password': self.user.password,
                'new_password': 'Is5!2345123454a',
                'confirm_password': 'Is5!2345123454a'},
            user=self.user,
            profile=self.profile)

        result = form.is_valid()

        self.assertEqual(expected, result)

    def test_return_form_invalid_if_not_contain_upper_and_lower(self):
        expected = False

        # change password using the password change form
        form1 = ChangePasswordForm(
            data={
                'current_password': self.user.password,
                'new_password': 'is5!2345123454a',
                'confirm_password': 'is5!2345123454a'},
            user=self.user,
            profile=self.profile)

        form2 = ChangePasswordForm(
            data={
                'current_password': self.user.password,
                'new_password': 'IS5!2345123454A',
                'confirm_password': 'IS5!2345123454A'},
            user=self.user,
            profile=self.profile)

        result1 = form1.is_valid()
        result2 = form2.is_valid()

        self.assertEqual(expected, result1)
        self.assertEqual(expected, result2)

    def test_return_form_invalid_if_not_contain_digits(self):
        expected = False

        # change password using the password change form
        form = ChangePasswordForm(
            data={
                'current_password': self.user.password,
                'new_password': 'IsTestAAAAAbb!bCCCCCCCC',
                'confirm_password': 'IsTestAAAAAbb!bCCCCCCCC'},
            user=self.user,
            profile=self.profile)

        result = form.is_valid()

        self.assertEqual(expected, result)

    def test_return_form_invalid_if_not_contain_special_characters(self):
        expected = False

        # change password using the password change form
        form = ChangePasswordForm(
            data={
                'current_password': self.user.password,
                'new_password': 'IsTestAAAAAbbbbCCCCCCCC',
                'confirm_password': 'IsTestAAAAAbbbbCCCCCCCC'},
            user=self.user,
            profile=self.profile)

        result = form.is_valid()

        self.assertEqual(expected, result)

    def test_return_form_invalid_if_new_and_confirm_pw_not_the_same(self):
        expected = False

        # change password using the password change form
        form = ChangePasswordForm(
            data={
                'current_password': self.user.password,
                'new_password': 'IsTestAAAAAbbbbCCCCCCCC',
                'confirm_password': 'IsTestAAAAAbbbbCCCCCCCC1'},
            user=self.user,
            profile=self.profile)

        result = form.is_valid()

        self.assertEqual(expected, result)