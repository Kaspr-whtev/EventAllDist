from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('eventnoti/', views.home, name="noti_home"),
    path('api/get_user/', views.get_user, name='get_user'),
    path('eventnoti/users/', views.show_users, name='show_users'),
]
