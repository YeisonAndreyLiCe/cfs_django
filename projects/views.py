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

def requirement_completed(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    project = Project.objects.get(id=request.POST['id_project'])
    requirements = File()
    info = requirements.openFile('requirements',project.requirements)
    lines = requirements.lines
    lines[int(request.POST['id_requirement'])] = lines[int(request.POST['id_requirement'])].strip() + "- Completed \n"
    new_lines = ("").join(lines)
    requirements.update(new_lines,'requirements', project.requirements, request.session['user_id'])
    return JsonResponse({'status':'success','id': request.POST['id_requirement'], 'info': lines[int(request.POST['id_requirement'])], 'route':"requirement_uncompleted", 'button': "Completed"})

def requirement_uncompleted(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    project = Project.objects.get(id=request.POST['id_project'])
    requirements = File()
    requirements.openFile('requirements',project.requirements)
    lines = requirements.lines
    lines[int(request.POST['id_requirement'])] = lines[int(request.POST['id_requirement'])].replace("- Completed \n", "\n")
    new_lines = ("").join(lines)
    requirements.update(new_lines,'requirements', project.requirements, request.session['user_id'])
    return JsonResponse({'status':'success','id': request.POST['id_requirement'], 'info': lines[int(request.POST['id_requirement'])], 'route':"requirement_completed", 'button': "Not Completed"})

def todo_task_uncompleted(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    project = Project.objects.get(id=request.POST['id_project'])
    todo = File()
    todo.openFile('ToDo',project.todo)
    lines = todo.lines
    lines[int(request.POST['id_task'])] = lines[int(request.POST['id_task'])].replace("- Completed \n", "\n")
    new_lines = ("").join(lines)
    todo.update(new_lines,'ToDo', project.todo, request.session['user_id'])
    return JsonResponse({'status':'success','id': request.POST['id_task'], 'info': lines[int(request.POST['id_task'])], 'route':"todo_task_completed", 'button': "Not Completed"})

def todo_task_completed(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    project = Project.objects.get(id=request.POST['id_project'])
    todo = File()
    info = todo.openFile('ToDo',project.todo)
    lines = todo.lines
    lines[int(request.POST['id_task'])] = lines[int(request.POST['id_task'])].strip() + "- Completed \n"
    new_lines = ("").join(lines)
    todo.update(new_lines,'ToDo', project.todo, request.session['user_id'])
    return JsonResponse({'status':'success','id': request.POST['id_task'], 'info': lines[int(request.POST['id_task'])], 'route':"todo_task_uncompleted", 'button': "Completed"})

def add_requirements(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    project = Project.objects.get(id=request.POST['id_project'])
    requirements = File()
    if requirements.validator(request.POST['new_requirements']):
        requirements.openFile('requirements',project.requirements)
        num_lines_before = len(requirements.lines)      
        project.requirements = requirements.addLines(request.POST['new_requirements'],'requirements', project.requirements, request.POST['user_id'])
        project.save()
        print(requirements.lines)
        return JsonResponse({'status': 'success','new_requirements': request.POST['new_requirements'], 'num_lines_before': num_lines_before, 'id_project': request.POST['id_project']})
    return JsonResponse({'status': 'error'})
    
def delete_requirement(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    project = Project.objects.get(id=request.POST['id_project'])
    requirements = File()
    requirements.openFile('requirements',project.requirements)
    requirements.deleteLine(int(request.POST['id_requirement']),'requirements', project.requirements)
    return JsonResponse({'status': 'delete', 'id': request.POST['id_requirement'],'lines': requirements.lines, 'id_project': request.POST['id_project']})

def add_todo_task(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    project = Project.objects.get(id=request.POST['id_project'])
    todo = File()
    if todo.validator(request.POST['new_tasks']):
        todo.openFile('ToDo',project.todo)
        num_lines_before = len(todo.lines)
        project.todo = todo.addLines(request.POST['new_tasks'],'ToDo', project.todo, request.POST['user_id'])
        project.save()
        return JsonResponse({'status': 'success','new_to_dos': request.POST['new_tasks'], 'num_lines_before': num_lines_before, 'id_project': request.POST['id_project']})
    return JsonResponse({'status': 'error'})

def delete_todo_task(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    project = Project.objects.get(id=request.POST['id_project'])
    todo = File()
    info = todo.openFile('ToDo',project.todo)
    todo.deleteLine(int(request.POST['id_task']),'ToDo', project.todo)
    return JsonResponse({'status': 'delete', 'id': request.POST['id_task'],'lines': todo.lines, 'id_project': request.POST['id_project']})

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
