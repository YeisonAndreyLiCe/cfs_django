import os

#from django.contrib import messages
import bcrypt
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.urls import reverse
from users.models import User

from .forms import RegisterForm
from .models import Cookie


def index(request):
    """ context = {
        'cookies': Cookie.objects.all()
    }
    return render(request, 'index.html', context) """
    return render(request, 'pre_login/index.html')

def login(request):
    return render(request, 'pre_login/login.html')

def logout(request):
    request.session.flush()
    return redirect('/')


def login_user(request):
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                route = reverse('users:projects')
                return JsonResponse({'route': route})
            else:
                return JsonResponse({'error': 'Invalid Password'})
        else:
            return JsonResponse({'error': "Invalid Email"})
    return redirect(reverse('pre_login:register'))

def get_api_key(request):
    if request.method == 'POST':
        key = os.environ.get('IPSTACK_API_KEY')
        return JsonResponse({'key': key})
    return redirect(reverse('pre_login:register'))

def set_cookies(request):
    if request.method == 'POST':
        if Cookie.validator(request.POST):
            return JsonResponse({'error': 'Invalid Cookie'})
        Cookie.objects.create(
            ip = request.POST['ip'],
            country = request.POST['country'],
            city = request.POST['city'],
        )
        Cookie.save()
        return JsonResponse({'success': 'success'})
    return redirect(reverse('pre_login:register'))


def register(request):
    if request.method == 'GET':
        register_form = RegisterForm()
        return render(request, 'pre_login/register_form.html', {'form': register_form})
    
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        if errors:
            data = {}
            for key, value in errors.items():
                data[key] = value
            return JsonResponse(data)
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password = pw_hash
            )
            request.session['user_id'] = user.id
            route = reverse("users:projects") 
            return JsonResponse({'route': route})
        return JsonResponse({'errors': register_form.errors.as_ul()})
    return redirect(reverse('pre_login:register'))