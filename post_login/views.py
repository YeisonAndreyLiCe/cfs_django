from multiprocessing import context
from django.shortcuts import render, redirect
import os
from pre_login.models import User
from .models import Project
from django.http import JsonResponse

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

def create_project(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    errors = Project.objects.validator(request.POST, request.FILES)
    if len(errors) > 0:
        data = {}
        for key, value in errors.items():
            data[key] = value
        return JsonResponse(data, status=400)
        #return redirect('/projects/<int:id>/new_project')
    else:
        Project.objects.create(
            name = request.POST['name'],
            public_status = request.POST['public_status'],
            description = request.POST['description'],
            wireframe = request.POST['wireframe'],
            user_flow_image = request.POST['user_flow_image'],
            owner = User.objects.get(id=request.session['user_id']),
        )
        return redirect('/projects/<int:id>/projects')