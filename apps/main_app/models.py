from django.db import models
import re

# Create your models here.


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "first name: at least 2 characters required"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "last name: at least 2 characters required"
        if not postData['first_name'].isalpha() or not postData['last_name'].isalpha():
            errors['name'] = "invalid name"
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'invalid email address!'
        for user in User.objects.all():
            if user.email == postData['email']:
                errors['email'] = "email already exist!"
        if len(postData['password']) < 6:
            errors['password'] = "password must be longer than 5 characters"
        if postData['password'] != postData['password_ver']:
            errors['password'] = "password does not match!"
        return errors


class WishManager(models.Manager):
    def wish_validator(self, postData):
        errors = {}
        if len(postData['wish']) < 3:
            errors['wish'] = "wish: at least 3 characters required"
        if len(postData['description']) < 3:
            errors['description'] = "description: at least 3 characters required"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # .wishes.all()


class Wish(models.Model):
    wish = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    granted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='wishes')
    likers = models.ManyToManyField(User, related_name='liked_wishes')
    objects = WishManager()

    def count_likes(self):
        return len(self.likers.all())
