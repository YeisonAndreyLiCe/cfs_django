from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Project
from users.models import User
import os

""" from .forms import UploadFileForm """
""" from django.core.files import File
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from datetime import datetime """

# Create your views here.
def projects_templates(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    return render(request, 'projects_templates.html')

def new_project(request,id):
    if 'user_id' not in request.session:
        return redirect('/login')
    return render(request, 'new_project.html')

def create_project(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    if request.method == "POST":
        errors = Project.objects.validator(request.POST)
        if len(errors) > 0:
            data = {}
            for key, value in errors.items():
                data[key] = value
            print(data)
            return JsonResponse(data)

        form = Project(request.POST, request.FILES)
        print(form)
        #if form.validator():
        project = Project.objects.create(
            name = request.POST['name'],
            public_status = request.POST['public_status'],
            description = request.POST['description'],
            wireframe = request.FILES['wireframe'],
            user_flow_image = request.FILES['user_flow_image'],
            owner = User.objects.get(id=request.session['user_id'])
        )
        project.save()
        route = '/users/'+str(request.session['user_id'])+'/view_project/'+str(project.id)
        print(JsonResponse({'route': route}))
        return JsonResponse({'route': route})
            
    return redirect('/users/new_user_project')

def edit(request, id):
    if 'user_id' not in request.session:
        return redirect('/login')
    context = {
        'project': Project.objects.get(id=id),
    }
    return render(request, 'edit.html', context)

def update(request, id):
    if 'user_id' not in request.session:
        return redirect('/login')
    if request.method == "POST":
        errors = Project.objects.validator(request.POST)
        if len(errors) > 0:
            data = {}
            for key, value in errors.items():
                data[key] = value
            print(data)
            return JsonResponse(data)
        project = Project.objects.get(id=id)
        project.name = request.POST['name']
        project.public_status = request.POST['public_status']
        project.description = request.POST['description']
        project.wireframe = request.FILES['wireframe']
        project.user_flow_image = request.FILES['user_flow_image']
        project.save()
        route = '/users/'+str(request.session['user_id'])+'/view_project/'+str(project.id)
        print(JsonResponse({'route': route}))
        return JsonResponse({'route': route})
    return redirect('/users/'+str(request.session['user_id'])+'/view_project/'+str(id))

def delete(request, id):
    if 'user_id' not in request.session:
        return redirect('/login')
    project = Project.objects.get(id=id)
    project.delete()
    return redirect('/users/'+str(request.session['user_id'])+'/projects')