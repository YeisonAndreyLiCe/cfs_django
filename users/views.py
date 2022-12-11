from django.shortcuts import render, redirect
from .models import User
from projects.models import Project
from django.urls import reverse


def projects(request):
    if 'user_id' not in request.session:
        return redirect(reverse("pre_login:login"))
    projects = Project.objects.filter(owner=request.session['user_id'])
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'projects': projects,
        'indexes': [i for i in range(len(projects))],
    }
    return render(request, 'users/user_projects.html', context) 


def new_user_project(request):
    if 'user_id' not in request.session:
        return redirect(reverse("pre_login:login"))
    return redirect(reverse("projects:new_project", args=(request.session["user_id"],)))