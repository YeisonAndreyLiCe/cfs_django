from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def logout(request):
    return render(request, 'register.html')

def register(request):
    return render(request, 'register.html')

def projects_templates(request):
    return render(request, 'projects_templates.html')