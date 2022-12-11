from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('projects', views.projects, name='projects'),
    path('new_user_project', views.new_user_project, name='new_user_project')  
]