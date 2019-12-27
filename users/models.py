from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# class UserManager(BaseUserManager):
#     def create_user(self,username, email, password):
#         if not email:
#             raise ValueError('User must provide an e-mail address')
#         if not username:
#           raise ValueError('User must provide an username address')

#         user = self.model(
#             email=self.normalize_email(email)
#         )

#         user.set_password(password)
#         user.save()

#         return user

#     def create_superuser(self, email, password=None):
#         user = self.create_user(email, password)

#         user.is_admin = True
#         user.save()

#         return user

class User(AbstractUser):
    """User model."""

    email = models.EmailField(('email address'), unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []




