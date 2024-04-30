from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
  email = models.EmailField(unique=True)
  
  # Add any additional fields you need
  is_qualified = models.BooleanField(
    default=False,
    help_text="Designates whether the user has taken the training course.",
  )
  is_email_verified = models.BooleanField(
    default=False,
    help_text="Designates whether the user has verfied their email.",
  )
    
