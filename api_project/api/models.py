from django.db import models

# Create your models here.
class book(models.Model):
    title = models.CharField(max_length = 255)
    author = models.CharField(max_length = 200)
    