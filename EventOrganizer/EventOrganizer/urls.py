"""
URL configuration for EventOrganizer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import EventViewSet, create_event_form, organizer_home_page, show_events, get_user, show_users

urlpatterns = [
    path('organizer/api/org_home', organizer_home_page, name='org_home'),
    path('organizer/api/events', EventViewSet.as_view({
        'get': 'list_events',
        'post': 'create_event',
    })),

    path('organizer/api/events/<str:pk>', EventViewSet.as_view({
        'get': 'get_event',
        'put': 'update_event',
        'delete': 'delete_event'
    })),
    path('organizer/api/create/', create_event_form, name='create-event'),
    path('organizer/api/show-events/', show_events, name='show-events'),
    path('organizer/api/events/<str:pk>/edit/', EventViewSet.as_view({
        'get': 'edit_event_form',
        'post': 'edit_event_form'
    }), name='edit_event'),
    path('api/events/<str:pk>/delete/', EventViewSet.as_view({
        'post': 'delete_event_form'
    }), name='delete_event'),
    path('api/events/<str:pk>/confirm_delete/', EventViewSet.as_view({
        'get': 'confirm_delete_event',
        'post': 'confirm_delete_event'
    }), name='confirm_delete_event'),
    path('api/get_user/', get_user, name='get_user'),
    path('organizer/users/', show_users, name='show_users'),



]
