from curses import use_default_colors
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Project
from users.models import User
import os
from .documents import File, Artefact
#from werkzeug.utils import secure_filename

# Create your views here.
def projects_templates(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    path = os.path.join('projects', 'templates')
        #os.makedirs(path)
    print(path)
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
            return JsonResponse(data)
        requirements = File()
        if requirements.validator(request.POST['requirements']):
            requirements.save(request.POST['requirements'],'requirements', request.session['user_id'])
        todo = File()
        if todo.validator(request.POST['todo']):
            todo.save(request.POST['todo'],'ToDo', request.session['user_id'])
        if not 'wireframe' in request.FILES:
            wireframe = None
        else:
            wireframe = request.FILES['wireframe']
        if not 'user_flow_image' in request.FILES:
            user_flow_image = None
        else:  
            user_flow_image = request.FILES['user_flow_image']
        project = Project.objects.create(
            name = request.POST['name'],
            public_status = request.POST['public_status'],
            description = request.POST['description'],
            wireframe = wireframe,
            user_flow_image = user_flow_image,
            requirements = requirements.name,
            todo = todo.name,
            owner = User.objects.get(id=request.session['user_id'])
        )
        project.save()
        route = '/users/'+str(request.session['user_id'])+'/view_project/'+str(project.id)
        return JsonResponse({'route': route})
            
    return redirect('/users/new_user_project')

def edit(request, id):
    if 'user_id' not in request.session:
        return redirect('/login')
    project = Project.objects.get(id =id)
    requirement = File()
    todo = File()
    requirement.openFile('requirements',project.requirements)
    todo.openFile('ToDo',project.todo)
    context = {
        'project': project,
        'requirements' : requirement.content,
        'todoList' : todo.content,
    } 
    return render(request, 'edit.html', context)

def update(request, id):
    if 'user_id' not in request.session:
        return redirect('/login')
    if request.method == "POST":
        errors = Project.objects.validator(request.POST)
        if errors:
            data = {}
            for key, value in errors.items():
                data[key] = value
            print(data)
            return JsonResponse(data)
        project = Project.objects.get(id=id)
        project.name = request.POST['name']
        project.public_status = request.POST['public_status']
        project.description = request.POST['description']
        requirements = File()
        if requirements.validator(request.POST['requirements']):
            project.requirements = requirements.update(request.POST['requirements'],'requirements',project.requirements, request.session['user_id'])
        todo = File()
        if todo.validator(request.POST['todo']):
            project.todo = todo.update(request.POST['todo'],'ToDo', project.todo, request.session['user_id'])
        project.save()
        #project.wireframe = request.FILES['wireframe']
        #project.user_flow_image = request.FILES['user_flow_image']
        route = f"/users/{request.session['user_id']}/view_project/{project.id}"
        return JsonResponse({'route': route})
    return redirect('/users/'+str(request.session['user_id'])+'/view_project/'+str(id))

def delete(request, id):
    if 'user_id' not in request.session:
        return redirect('/login')
    project = Project.objects.get(id=id)
    file = File()
    file.deleteFile('requirements',project.requirements)
    file.deleteFile('ToDo',project.todo)
    try:
        os.remove(project.wireframe.path)
    except ValueError:
        pass
    try:
        os.remove(project.user_flow_image.path)
    except ValueError:
        pass
    project.delete()
    return redirect(f"/users/{request.session['user_id']}/projects")


def update_feature(request, id, file, status, id_project):
    if 'user_id' not in request.session:
        return redirect('/login')
    project = Project.objects.get(id=id_project)
    todo = File()
    if file == 'requirements':
        todo.openFile('requirements',project.requirements)
    else:
        todo.openFile('ToDo',project.todo)
    lines = todo.lines
    if status == "Completed":
        lines[int(id)] = lines[int(id)].strip() + "- Completed \n"
        route = "uncompleted"
    else:
        lines[int(id)] = lines[int(id)].replace("- Completed \n", "\n")
        route = "completed"
    new_lines = ("").join(lines)
    todo.update(new_lines,file, project.todo, request.session['user_id'])
    return JsonResponse({'status':status,'type':file,'id': id, 'info': lines[int(id)], 'route':route, 'button': route.capitalize()})


def add_features(request, file_class):
    if 'user_id' not in request.session:
        return redirect('/login')
    project = Project.objects.get(id=request.POST['id_project'])
    file = File()
    if file.validator(request.POST[file_class]):
        if file_class == 'new_requirements':
            file.openFile('requirements',project.requirements) 
            project.requirements = file.addLines(request.POST['new_requirements'],'requirements', project.requirements, request.POST['user_id'])
            project.save()
        else:
            file.openFile('ToDo',project.todo)
            project.todo = file.addLines(request.POST['new_tasks'],'ToDo', project.todo, request.POST['user_id'])
            project.save()
        num_lines_before = len(file.lines)
        return JsonResponse({'status': 'success','info': request.POST[file_class], 'num_lines_before': num_lines_before, 'id_project': request.POST['id_project']})
    return JsonResponse({'status': 'error'})

def delete_feature(request, id, file_class, id_project):
    if 'user_id' not in request.session:
        return redirect('/login')
    project = Project.objects.get(id=id_project)
    file = File()
    if file_class == 'requirements':
        file.openFile('requirements',project.requirements)
        file.deleteLine(int(id),file_class, project.requirements)
    else:
        file.openFile('ToDo',project.todo)
        file.deleteLine(int(id),file_class, project.todo)
    return JsonResponse({'type': file_class, 'id': id,'lines': file.lines, 'id_project': id_project})

def add_user_flow_image(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    project = Project.objects.get(id=request.POST['id_project'])
    try:
        project.user_flow_image = request.FILES['user_flow_image']
        project.save()
    except:
        pass
    return redirect(f"/users/{request.session['user_id']}/view_project/{request.POST['id_project']}")
    #return JsonResponse({"route": f"/users/{request.session['user_id']}/view_project/{request.POST['id_project']}"})

def delete_user_flow_image(request, id):
    if 'user_id' not in request.session:
        return redirect('/login')
    project = Project.objects.get(id=id)
    os.remove(project.user_flow_image.path)
    project.user_flow_image = ""
    project.save()
    return redirect(f"/users/{request.session['user_id']}/view_project/{id}")

def add_wireframe(request, id):
    if 'user_id' not in request.session:
        return redirect('/login')
    project = Project.objects.get(id=id)
    try:
        project.wireframe = request.FILES['wireframe']
        project.save()
    except:
        pass
    return redirect(f"/users/{request.session['user_id']}/view_project/{id}")

def delete_wireframe(request, id):
    if 'user_id' not in request.session:
        return redirect('/login')
    project = Project.objects.get(id=id)
    os.remove(project.wireframe.path)
    project.wireframe = ""
    project.save()
    return redirect(f"/users/{request.session['user_id']}/view_project/{id}")
