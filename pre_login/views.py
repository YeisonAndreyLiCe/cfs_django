from django.shortcuts import render, redirect
import os
from .models import User
from django.contrib import messages
import bcrypt

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
        errors = User.objects.validator(request.POST)
        print(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
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
            return redirect('/users/projects_templates')
    else:
        return redirect('/register')

def login_user(request):
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/users/projects')
            else:
                messages.error(request, 'Invalid email/password')
                return redirect('/login')
    return redirect('/login')