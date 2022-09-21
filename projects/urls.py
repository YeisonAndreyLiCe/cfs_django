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
]