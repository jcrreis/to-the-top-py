from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class User(AbstractUser):
    """User model."""

    email = models.EmailField(('email address'), unique=True)
    image = models.ImageField(upload_to='users',null=True, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']




