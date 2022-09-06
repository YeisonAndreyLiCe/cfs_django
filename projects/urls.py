from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/new_project', views.new_project, name='new_project'),
    path('create_project', views.create_project, name='create_project'),
    path('projects_templates', views.projects_templates, name='projects_templates'),
    path('<int:id>/edit', views.edit, name='edit'),
    path('<int:id>/update', views.update, name='update'),
    path('<int:id>/delete', views.delete, name='delete'),
]