#from multiprocessing import context
from django.shortcuts import render, redirect
from .models import User
from django.http import JsonResponse
from projects.models import Project
import os
from projects.documents import OpenF

# Create your views here.
def projects(request, id):
    if 'user_id' not in request.session:
        return redirect('/login')
    projects = Project.objects.filter(owner=request.session['user_id'])
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'projects': projects,
        'indexes': [i for i in range(len(projects))],
    }
    print(context['indexes'])
    return render(request, 'user_projects.html', context)  
    #return render(request, 'create_project.html')


def new_user_project(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    return redirect('/projects/'+str(request.session['user_id'])+'/new_project')

def view_project(request, id_user, id_project):
    if 'user_id' not in request.session:
        return redirect('/login')
    #user = User.objects.get(id=request.session['user_id'])
    project = Project.objects.get(id =id_project)
    requirements = OpenF()
    todo = OpenF()

    context = {
        'project': project,
        'requirements' : requirements.Open('requirements',project.requirements),
        'to_dos' : todo.Open('ToDo',project.todo),
    }
    return render(request, 'view_user_project.html', context)