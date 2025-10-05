from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    stats = models.JSONField(default=dict, blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True)
    def __str__(self): return self.username

    def get_profile_photo_url(self):
        if self.profile_photo and hasattr(self.profile_photo, 'url'):
            return self.profile_photo.url
        return '/static/hackathon/images/default-user.jpg'

class ForumCategory(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class ForumThread(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    def __str__(self): return self.title

class ForumPost(models.Model):
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Post in {self.thread}"

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='news/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    def __str__(self): return self.title

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    skills = models.CharField(max_length=200)
    contributions = models.TextField()
    contact = models.EmailField()
    social_media = models.URLField(blank=True)
    photo = models.ImageField(upload_to='team/', blank=True)
    def __str__(self): return self.name
