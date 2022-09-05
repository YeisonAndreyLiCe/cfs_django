from __future__ import unicode_literals
from django.db import models

from django.db import models
import re

class UserManager(models.Manager):
    def validator(self, postData):
        re_password = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')
        re_email = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['first_name']) < 3:
            errors["first_name"] = "Name should be at least 3 characters"
        if len(postData['last_name']) < 3:
            errors["last_name"] = "Name should be at least 3 characters"
        if not re_email.match(postData['email']):
            errors["email"] = "Invalid email address"
        if not re_password.match(postData['password']):
            errors["password"] = "Password must be at least 8 characters, contain at least one number, one uppercase and one lowercase letter"
        if postData['password'] != postData['confirm_password']:
            errors["confirm_password"] = "Passwords do not match"
        if User.objects.filter(email=postData['email']):
            errors["email"] = "Email already exists"
        return errors

    def credentials(self, postData):
        errors = {}
        if not postData['email']:
            errors["email"] = "Email is required"
        if not postData['password']:
            errors["password"] = "Password is required"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() # now User.validator() is a function that takes postData and returns errors

    def __str__(self):
        return self.first_name