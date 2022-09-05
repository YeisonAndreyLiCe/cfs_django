from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('projects_templates', views.projects_templates, name='projects_templates'),
    path('project/<int:id>', views.project, name='project'),
    path('projects', views.projects, name='projects'),
]