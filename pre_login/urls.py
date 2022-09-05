from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('register_user/', views.register_user, name='register_user'),
    path('login_user/', views.login_user, name='login_user'),
]