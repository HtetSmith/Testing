from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser,Group


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    )
    email = models.EmailField(unique=True, blank=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    linked_accounts = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class MediaItem(models.Model):
    title = models.CharField(max_length=255)  # Title of the media
    description = models.TextField(blank=True, null=True)  # Optional description
    image = models.ImageField(upload_to='courses/images/', blank=True, null=True)  # Image upload
    video = models.FileField(upload_to='courses/videos/', blank=True, null=True)  # Video upload
    url = models.URLField(blank=True, null=True)  # URL field for links
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-add timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Auto-update timestamp

    def __str__(self):
        return self.title