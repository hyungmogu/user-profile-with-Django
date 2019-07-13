from django.db import models

from django.contrib.auth.models import User


class Profile(User):
    date_of_birth = models.DateField()
    confirm_email = models.EmailField()
    short_bio = models.TextField()
    avatar = models.ImageField(upload_to='images/')