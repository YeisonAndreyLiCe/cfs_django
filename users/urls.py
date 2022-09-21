from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/projects', views.projects, name='projects'),
    path('new_user_project', views.new_user_project, name='new_user_project'),
    path('<int:id_user>/view_project/<int:id_project>', views.view_project, name='view_project'),   
]