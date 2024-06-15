from django.urls import path
from . import views


urlpatterns = [
    path('eventauth/', views.home, name=""),
    path('eventauth/logout', views.logout_view, name="user-logout"),
    path('eventauth/register', views.register, name="register"),
    path('eventauth/my-login', views.my_login, name="my-login"),
    path('eventauth/dashboard', views.dashboard, name="dashboard"),
    path('eventauth/verify-token/', views.verify_token, name='verify_token'),
]