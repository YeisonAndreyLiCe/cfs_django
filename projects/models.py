from __future__ import unicode_literals
from django.db import models
import re
from users.models import User

class ProjectManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors["name"] = "Name should be at least 3 characters"
        if len(postData['description']) < 10:
            errors["description"] = "Description should be at least 10 characters"
        """ if len(postData['wireframe']) < 3:
            errors["wireframe"] = "Wireframe should be at least 3 characters"
        if len(postData['user_flow_image']) < 3:
            errors["user_flow_image"] = "User flow image should be at least 3 characters" """
        return errors

class Project(models.Model):
    name = models.CharField(max_length=100)
    public_status = models.BooleanField(default=False)
    description = models.CharField(max_length=1000)
    requirements = models.CharField(max_length=1000, null=True)   
    todo = models.CharField(max_length=1000, null=True)
    wireframe = models.FileField(upload_to='wireframes/', blank=True, null=True)
    user_flow_image = models.ImageField(upload_to='user_flows/', blank=True, null=True)
    owner = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)
    contributors = models.ManyToManyField(User, related_name='contributors')
    favorite = models.ManyToManyField(User, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProjectManager()