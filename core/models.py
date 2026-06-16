from django.db import models
# pyrefly: ignore [missing-import]
from ckeditor.fields import RichTextField

from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Topic(models.Model):
    name = models.CharField(max_length=155, unique=True)
    description = models.TextField(blank=True, null=True)
    icon_name = models.CharField(max_length=50, blank=True, null=True, help_text="Material symbol name (e.g., 'memory', 'palette')")

    def __str__(self):
        return self.name


class CreatePost(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    topic=models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    cover_image_url = models.URLField(max_length=500, blank=True, null=True)
    cover_image = models.ImageField(upload_to='post_covers/', blank=True, null=True)
    content=RichTextField()
    view_count=models.PositiveBigIntegerField(default=0)
    liked_users=models.ManyToManyField(User,related_name='liked_post',blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_featured=models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.liked_users.count()

class Comment(models.Model):
    content=models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(CreatePost,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
