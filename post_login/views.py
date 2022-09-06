from multiprocessing import context
from django.shortcuts import render, redirect
import os
from pre_login.models import User
from .models import Project

# Create your views here.
def projects(request, id):
    if 'user_id' not in request.session:
        return redirect('/login')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'projects': Project.objects.filter(owner=request.session['user_id']),
    }
    return render(request, 'projects.html', context)  
    #return render(request, 'create_project.html')

def projects_templates(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    return render(request, 'projects_templates.html')

def project(request, id):
    if 'user_id' not in request.session:
        return redirect('/login')
    return render(request, 'project.html')

def new_project(request,id):
    if 'user_id' not in request.session:
        return redirect('/login')
    return render(request, 'new_project.html')