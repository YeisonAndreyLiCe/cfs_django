from django.urls import path
from . import views

app_name = 'pre_login'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('login_user/', views.login_user, name='login_user'),
    path('get_api_key/', views.get_api_key, name='get_api_key'),
    path('set_cookies/', views.set_cookies, name='set_cookies'),
]