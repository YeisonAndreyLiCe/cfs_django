from django.shortcuts import render, redirect
import os
from users.models import User
#from django.contrib import messages
import bcrypt
from django.http import JsonResponse
from .models import Cookie

def index(request):
    """ context = {
        'cookies': Cookie.objects.all()
    }
    return render(request, 'index.html', context) """
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
            route = '/users/'+str(user.id)+'/projects'
            return JsonResponse({'route': route})
            #return redirect('/users/projects_templates')
    else:
        return redirect('/register')

def login_user(request):
    print(request.POST)
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                route = '/users/'+str(logged_user.id)+'/projects'
                return JsonResponse({'route': route})
            else:
                return JsonResponse({'error': 'Invalid Password'})
        else:
            return JsonResponse({'error': "Invalid Email"})
    return redirect('/register')

def get_api_key(request):
    print(request.POST)
    if request.method == 'POST':
        key = os.environ.get('IPSTACK_API_KEY')
        print(key)
        return JsonResponse({'key': key})
    return redirect('/register')

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
    return redirect('/register')