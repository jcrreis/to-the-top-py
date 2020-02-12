from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class User(AbstractUser):
    """User model."""
    def validate_image(fieldfile_obj):
      filesize = fieldfile_obj.file.size
      megabyte_limit = 10.0
      if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    email = models.EmailField(('email address'), unique=True)
    image = models.ImageField(upload_to='users',null=True, blank=True, validators=[validate_image])
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']




