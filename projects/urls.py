from cmath import phase
from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/new_project', views.new_project, name='new_project'),
    path('create_project', views.create_project, name='create_project'),
    path('projects_templates', views.projects_templates, name='projects_templates'),
    path('<int:id>/edit', views.edit, name='edit_project'),
    path('<int:id>/update', views.update, name='update_project'),
    path('<int:id>/delete', views.delete, name='delete_project'),
    path('requirement_completed', views.requirement_completed, name='requirement_completed'),
    path('requirement_uncompleted', views.requirement_uncompleted, name='requirement_uncompleted'),
    path('delete_requirement', views.delete_requirement, name='delete_requirement'),
    path('add_requirements', views.add_requirements, name='add_requirements'),
    path('add_todo_task', views.add_todo_task, name='add_todo_task'),
    path('delete_todo_task', views.delete_todo_task, name='delete_todo_task'),
    """ path('todo_task_completed', views.todo_task_completed, name='todo_task_completed'),
    path('todo_task_uncompleted', views.todo_task_uncompleted, name='todo_task_uncompleted'), """
    path('add_user_flow_image', views.add_user_flow_image, name='add_user_flow_image'),
    path('<int:id>/delete_user_flow_image', views.delete_user_flow_image, name='delete_user_flow_image'),
    path('<int:id>/add_wireframe', views.add_wireframe, name='add_wireframe'),
    path('<int:id>/delete_wireframe', views.delete_wireframe, name='delete_wireframe'),
]