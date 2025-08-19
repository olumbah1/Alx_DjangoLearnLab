from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='Images', blank=True, null=True)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following', 
        blank=True      # Self-referencing ManyToManyField to allow users to follow other users.
    )
    following = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='followed_by')
        
    def __str__(self):
        return self.username
    
    def follow_user(self, user):
         if user != self:
             self.following.add.user
             self.followers.add.self
    
    def unfollow_user(self, user):
        self.following.remove.user
        self.followers.remove.self
    
    def is_following(self, user):   # Check if current user is following another user
        return self.following.filter(id=user.id).exists()

    def is_followed_by(self, user): # Check if current user is followed by another user
        return self.followers.filter(id=user.id).exists()
    
    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count() 