from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData["first_name"]) == 0:
            errors["first_name"] = "The first name field is required"
        elif postData["first_name"].isalpha() == False:
            errors["first_name"] = "First name can only use letters"
        if len(postData["username"]) == 0:
            errors["username"] = "The username field is required"
        elif len(User.objects.filter(username=postData['username'])) > 0:
            errors['user'] = "This user already exists"
        if len(postData['last_name']) == 0:
            errors["last_name"] = "The last name field is required"
        elif postData['last_name'].isalpha() == False:
            errors["last_name"] = "Last name can only use letters"
        if len(postData['password']) == 0:
            errors["password"] = "The password field is required"
        elif len(postData['password']) < 8:
            errors["password"] = "Password must have at least 8 characters"
        elif postData['password'] != postData['confirm_password']:
            errors["password"] = "Password must be the same as the confirmed password"
        return errors

    def login_validator(self, postData):
        errors={}
        if len(postData["username"]) == 0:
            errors["username"] = "The username field is required"
        elif len(User.objects.filter(username=postData['username'])) == 0:
            errors['user'] = "User does not exist"
        elif len(User.objects.filter(username=postData['username'])) != 0:
            user = User.objects.get(username=postData['username'])
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()) == False:
                errors['password'] = "Password is incorrect"
        return errors

class PostManager(models.Manager):
    def post_validator(self, postData, fileData):
        errors={}
        if not postData["title"]:
            errors["title"] = "The title field is required"
        if not postData['desc']:
            errors['desc'] = "The description field is required"
        if not fileData['image']:
            errors['file'] = "That file is not valid"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    admin = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Post(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    image = models.ImageField(upload_to='images/')
    likes = models.SmallIntegerField()
    dislikes = models.SmallIntegerField()
    favorited_by_users = models.ManyToManyField(User, related_name="favorite_posts", blank=True)
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostManager()

class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', related_name ="comments", on_delete=models.CASCADE, blank=True, null=True)
    likes = models.SmallIntegerField()
    dislikes = models.SmallIntegerField()
    favorited_by_users = models.ManyToManyField(User, related_name="favorite_comments", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
