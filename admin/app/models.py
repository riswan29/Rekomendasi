from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='img_profile/')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
