from django.urls import path
from . import views

urlpatterns = [
    path('users', views.index, name='index'),
    path('users/login', views.login, name='login'),
    path('users/logout', views.logout, name='logout'),
    path('users/register', views.register, name='register'),
]