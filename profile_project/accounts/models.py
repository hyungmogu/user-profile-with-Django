from django.db import models

from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="user")
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(blank=True)
    confirm_email = models.EmailField(blank=True)
    short_bio = models.TextField(
        blank=True,
        validators=[
            MinLengthValidator(10, 'Entry must be 10 characters or longer')
            ])
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)