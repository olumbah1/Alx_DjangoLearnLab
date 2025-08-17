from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    tags = TaggableManager()  # TaggableManager adds tagging support
    def __str__(self):
        return self.title
        
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # If a user is deleted, their profile is deleted too.
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True) #Extra info you can store beyond what the default User model provides.
    
    def __str__(self):
        return f"{self.user.username} Profile"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.post
    
class Tag(models.Model):
    name = models.CharField(max_length=200)
    post = models.ManyToManyField(Post) 
    