from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name=""),
    path('logout', views.logout_view, name="user-logout"),
    path('register', views.register, name="register"),
    path('my-login', views.my_login, name="my-login"),
    path('dashboard', views.dashboard, name="dashboard"),

]