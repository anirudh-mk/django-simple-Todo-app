from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login, name="loginPage"),
    path('register', views.register, name="loginPage"),
    path('home', views.home, name="loginPage"),
    path('logout', views.logout, name='LogoutButton'),
    path('complete', views.complete, name='taskCompleteButton'),
    path('delete', views.delete, name='taskCompleteDelete'),
]

