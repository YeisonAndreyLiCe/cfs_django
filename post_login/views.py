from django.shortcuts import render, redirect
import os

# Create your views here.
def projects(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    return render(request, 'create_project.html')

def projects_templates(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    return render(request, 'projects_templates.html')

def project(request, id):
    if 'user_id' not in request.session:
        return redirect('/login')
    return render(request, 'project.html')

def projects(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    return render(request, 'project.html')