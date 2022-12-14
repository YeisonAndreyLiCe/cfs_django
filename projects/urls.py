from cmath import phase
from django.urls import path
from . import views

app_name = 'projects'
urlpatterns = [
    path('<int:id>/new_project', views.new_project, name='new_project'),
    path('create_project', views.create_project, name='create_project'),
    #path('projects_templates', views.projects_templates, name='projects_templates'),
    path('<int:id>/edit', views.edit, name='edit_project'),
    path('<int:id>/update', views.update, name='update_project'),
    path('<int:id>/delete', views.delete, name='delete_project'),
    path('delete/requirement/<int:id>/<int:id_project>', views.delete_requirement, name='delete_requirement'),
    path('delete/task/<int:id>/<int:id_project>', views.delete_task, name='delete_task'),
    path('update_feature/<int:id>/<str:file>/<str:status>/<int:id_project>', views.update_feature, name='update_feature'),
    path('add_features/<str:file_class>', views.add_features, name='add_features'),
    path('add_tasks/<int:id>', views.add_tasks, name='add_tasks'),
    path('add_requirements/<int:id>', views.add_requirements, name='add_requirements'),
    path('add_user_flow_image', views.add_user_flow_image, name='add_user_flow_image'),
    path('<int:id>/delete_user_flow_image', views.delete_user_flow_image, name='delete_user_flow_image'),
    path('<int:id>/add_wireframe', views.add_wireframe, name='add_wireframe'),
    path('<int:id>/delete_wireframe', views.delete_wireframe, name='delete_wireframe'),
    path('public_projects', views.public_projects, name='public_projects'),
    path('public_projects/<int:id>', views.view_public_project, name='view_public_project'),
    path('view_project/<int:project_id>', views.view_project, name='view_project')
]