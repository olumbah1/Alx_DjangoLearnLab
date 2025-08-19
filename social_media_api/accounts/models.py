from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_profile = models.ImageField(upload_to='Images', blank=True, null=True)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following', 
        blank=True      # Self-referencing ManyToManyField to allow users to follow other users.
    )
    def __str__(self):
        return self.username
    