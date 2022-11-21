#from curses import use_default_colors
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Project
from users.models import User
import os
from .documents import File, Artefact
from django.urls import reverse
#from werkzeug.utils import secure_filename

# Create your views here.
def projects_templates(request):
    if 'user_id' not in request.session:
        return redirect(reverse("pre_login:login"))
    path = os.path.join('projects', 'projects/templates')
        #os.makedirs(path)
    return render(request, 'projects/projects_templates.html')

def new_project(request,id):
    if 'user_id' not in request.session:
        return redirect(reverse("pre_login:login"))
    return render(request, 'projects/new_project.html')

def create_project(request):
    if 'user_id' not in request.session:
        return redirect(reverse("pre_login:login"))
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
        route = reverse("users:view_project", args=(request.session["user_id"], project.id))    #'/users/'+str(request.session['user_id'])+'/view_project/'+str(project.id)
        return JsonResponse({'route': route})
            
    return redirect(reverse("users:new_user_project"))

def edit(request, id):
    if 'user_id' not in request.session:
        return redirect(reverse("pre_login:login"))
    project = get_object_or_404(Project, id=id)
    requirement = File()
    todo = File()
    requirement.openFile('requirements',project.requirements)
    todo.openFile('ToDo',project.todo)
    context = {
        'project': project,
        'requirements' : requirement.content,
        'todoList' : todo.content,
    } 
    return render(request, 'projects/edit.html', context)

def update(request, id):
    if 'user_id' not in request.session:
        return redirect(reverse("pre_login:login"))
    if request.method == "POST":
        errors = Project.objects.validator(request.POST)
        if errors:
            data = {}
            for key, value in errors.items():
                data[key] = value
            return JsonResponse(data)
        project =  get_object_or_404(Project, id=id) #Project.objects.get(id=id)
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
        route = reverse("users:view_project", args=(request.session["user_id"], project.id))    #f"/users/{request.session['user_id']}/view_project/{project.id}"
        return JsonResponse({'route': route})
    return redirect(reverse("projects:edit_project", args=(request.session["user_id"], id)))  

def delete(request, id):
    if 'user_id' not in request.session:
        return redirect('/login')
    project = get_object_or_404(Project, id=id)
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
    return redirect(reverse("users:projects", args=(request.session["user_id"],)))  


def update_feature(request, id, file, status, id_project):
    if 'user_id' not in request.session:
        return redirect(reverse("pre_login:login"))
    project = get_object_or_404(Project, id=id_project)
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
        return redirect(reverse("pre_login:login"))
    project = get_object_or_404(Project, id=request.POST['id_project'])
    file = File()
    if file.validator(request.POST[file_class]):
        if file_class == 'new_requirements':
            project.requirements = file.addLines(request.POST['new_requirements'],'requirements', project.requirements, request.POST['user_id'])
            project.save()
        else:
            project.todo = file.addLines(request.POST['ToDo'],'ToDo', project.todo, request.POST['user_id'])
            project.save()
            file_class = 'ToDo'
        num_lines_before = len(file.lines)
        del file
        return JsonResponse({'type':file_class,'status': 'success','lines': request.POST[file_class].split("\r\n"), 'num_lines_before': num_lines_before, 'id_project': request.POST['id_project']})
    return JsonResponse({'status': 'error'})

def delete_feature(request, id, file_class, id_project):
    if 'user_id' not in request.session:
        return redirect(reverse("pre_login:login"))
    project = get_object_or_404(Project, id=id_project)
    file = File()
    if file_class == 'requirements':
        file.openFile('requirements',project.requirements)
        file.deleteLine(int(id),file_class, project.requirements)
    else:
        file.openFile('ToDo',project.todo)
        file.deleteLine(int(id),'ToDo', project.todo)
    return JsonResponse({'type': file_class, 'id': id,'lines':file.lines, 'id_project': id_project})

def add_user_flow_image(request):
    if 'user_id' not in request.session:
        return redirect(reverse("pre_login:login"))
    project = get_object_or_404(Project, id=request.POST['id_project']) # Project.objects.get(id=request.POST['id_project'])
    try:
        project.user_flow_image = request.FILES['user_flow_image']
        project.save()
    except:
        pass
    return redirect(reverse("users:view_project", args=(request.session['user_id'],request.POST["id_project"],)))
    #f"/users/{request.session['user_id']}/view_project/{request.POST['id_project']}"

def delete_user_flow_image(request, id):
    if 'user_id' not in request.session:
        return redirect(reverse("pre_login:login"))
    project =  get_object_or_404(Project, id=id)
    os.remove(project.user_flow_image.path)
    project.user_flow_image = ""
    project.save()
    return redirect(reverse("users:view_project", args=(request.session['user_id'],id,)))

def add_wireframe(request, id):
    if 'user_id' not in request.session:
        return redirect(reverse("pre_login:login"))
    project = get_object_or_404(Project, id=id)
    try:
        project.wireframe = request.FILES['wireframe']
        project.save()
    except:
        pass
    return redirect(reverse("users:view_project", args=(request.session['user_id'],id,)))

def delete_wireframe(request, id):
    if 'user_id' not in request.session:
        return redirect(reverse("pre_login:login"))
    project = get_object_or_404(Project, id=id)
    os.remove(project.wireframe.path)
    project.wireframe = ""
    project.save()
    return redirect(reverse("users:view_project", args=(request.session['user_id'],id,)))
