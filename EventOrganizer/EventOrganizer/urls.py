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
from .views import EventViewSet, create_event_form, organizer_home_page

urlpatterns = [
    path('api/org_home', organizer_home_page, name='org_home'),
    path('api/events', EventViewSet.as_view({
        'get': 'list_events',
        'post': 'create_event',
    })),

    path('api/events/<str:pk>', EventViewSet.as_view({
        'get': 'get_event',
        'put': 'update_event',
        'delete': 'delete_event'
    })),
    path('api/create/', create_event_form, name='create-event'),

]
