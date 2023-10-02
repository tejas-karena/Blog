from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    country = models.CharField(max_length=100)
    birth_date = models.DateField(blank=True, null=True)
    status = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager() 

    def __str__(self):
        return self.email
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    blog = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    #TODO:Rename to user
    username = models.ForeignKey(User,on_delete=models.CASCADE,related_name="ucomments") 
    #TODO: Rename to Blog
    commentblog = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    comment = models.TextField(blank=True, null=True)
    comment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment[:75] if len(self.comment) > 75 else self.comment







