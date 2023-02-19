from __future__ import unicode_literals
from django.db import models
import re
from users.models import User



class ProjectManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if not postData.get('name') or len(postData.get('name')) < 3:
            errors["name"] = "Name should be at least 3 characters"
        if not postData.get('description') or len(postData.get('description')) < 10:
            errors["description"] = "Description should be at least 10 characters"
        return errors

class Project(models.Model):
    PUBLIC_STATUS_CHOICES = (
        (True, 'Public'),
        (False, 'Private')
    )
    name = models.CharField(max_length=100, help_text="Project name")
    public_status = models.BooleanField(default=False, choices=PUBLIC_STATUS_CHOICES, help_text="Public or private project")
    description = models.CharField(max_length=1000, help_text="Project description")
    requirements = models.CharField(max_length=1000, null=True, help_text="Project requirements")   
    todo = models.CharField(max_length=1000, null=True, help_text="Project To Do list")
    wireframe = models.FileField(upload_to='wireframes/', blank=True, null=True, help_text="Project image")
    user_flow_image = models.ImageField(upload_to='user_flows/', blank=True, null=True, help_text="Project video")
    owner = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE, help_text="Project owner")
    contributors = models.ManyToManyField(User, related_name='contributors', help_text="Project contributors")
    favorite = models.ManyToManyField(User, related_name='favorites', help_text="Favorite projects")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProjectManager()