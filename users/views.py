#from multiprocessing import context
from tabnanny import check
from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.http import JsonResponse
from projects.models import Project
import os
from projects.documents import File, Artefact
from django.urls import reverse

# Create your views here.
def projects(request, id):
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

def view_project(request, id_user ,id_project):
    if 'user_id' not in request.session:
        return redirect(reverse("pre_login:login"))
    project = get_object_or_404(Project, id=id_project)
    requirements = File()
    todo = File()
    requirements = requirements.openFile('requirements',project.requirements)
    to_dos = todo.openFile('ToDo',project.todo)
    context = {
        'project': project,
        'requirements' : [Artefact(key, value) for key, value in requirements.items()],
        'to_dos' : [Artefact(key, value) for key, value in to_dos.items()],
    }
    return render(request, 'users/view_user_project.html', context)