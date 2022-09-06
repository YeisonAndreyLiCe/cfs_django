from django.shortcuts import render, redirect
import os
from .models import User
from django.contrib import messages
import bcrypt
from django.http import JsonResponse
# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def logout(request):
    request.session.flush()
    return redirect('/')

def register(request):
    return render(request, 'register.html')

def register_user(request):
    if request.method == 'POST':
        data = {}
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                data[key] = value
            print(data)
            return JsonResponse(data)
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password = pw_hash
            )
            request.session['user_id'] = user.id
            return JsonResponse({'user_id': user.id, 'route': '/projects'})
            #return redirect('/users/projects_templates')
    else:
        return redirect('/register')

def login_user(request):
    if request.method == 'POST':
        print(request.POST)
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return JsonResponse({'user_id': logged_user.id, 'route': '/projects'})
            else:
                return JsonResponse({'error': 'Invalid Password'})
        else:
            return JsonResponse({'error': "Invalid Email"})
    return redirect('/login')