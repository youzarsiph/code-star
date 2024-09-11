""" Data models for code_star.users """

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """CodeStar users"""

    picture = models.ImageField(
        null=True,
        blank=True,
        upload_to="images/users/",
        help_text="Profile picture",
    )
