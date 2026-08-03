from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model, extendable later without breaking things."""
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username

class Contact(models.Model):
    full_name = models.CharField(max_length=150)
    subject = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.subject}"


class Skill(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    level = models.IntegerField(default=100)

    def __str__(self):
        return self.name
    
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    github_url = models.URLField()
    live_demo = models.URLField(blank=True)
    technologies = models.CharField(max_length=255)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
