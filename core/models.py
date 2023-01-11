from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile',blank=False, default='timeline-1.jpg')
    locations = models.CharField(max_length=200,blank=True)

    
    def __str__(self) -> str:
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True,default = uuid.uuid4)
    user = models.CharField(max_length=200)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    no_of_likes = models.IntegerField(default=0)
    like_post_username =models.CharField(max_length=200)

    
    
    def __str__(self) -> str:
        return self.user


class LikePost(models.Model):
    post_id = models.CharField(max_length=200)
    username =models.CharField(max_length=200) 
    
    def __str__(self) -> str:
        return self.username

class FollowersCount(models.Model):
    follower =models.CharField(max_length=2000)
    user = models.CharField(max_length=200)
    
    def __str__(self):
        return self.user
    