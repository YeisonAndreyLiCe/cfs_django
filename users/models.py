from __future__ import unicode_literals
from django.db import models
import re

class UserManager(models.Manager):
    def validator(self, postData):
        re_password = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')
        re_email = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if not postData.get('first_name') or len(postData.get('first_name')) < 3:
            errors["first_name"] = "First Name should be at least 3 characters"
        if not postData.get('last_name') or len(postData.get('last_name')) < 3:
            errors["last_name"] = "Last Name should be at least 3 characters"
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
        if not postData.get('email'):
            errors["email"] = "Email is required"
        if not postData.get('password'):
            errors["password"] = "Password is required"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() # now User.validator() is a function that takes postData and returns errors

    """ class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(password__regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$'), name='password_regex'),
            models.CheckConstraint(check=models.Q(email__regex=r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'), name='email_regex'),
            models.UniqueConstraint(fields=['email'], name='unique_email')
        ] """

    def __str__(self):
        return self.email