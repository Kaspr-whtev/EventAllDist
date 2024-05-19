"""
URL configuration for EventParticipant project.

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
from django.urls import path, include
from .views import participant_home_page, show_events, show_event_details, payment_failed, payment_successful, get_event

urlpatterns = [
    path('participant/api/par_home', participant_home_page, name='org_home'),
    path('participant/api/show-events/', show_events, name='show-events'),
    path('participant/api/get_event/', get_event, name='get_event'),
    path('participant/api/show-events/<int:event_id>', show_event_details, name='show_event_details'),
    path('api/payment-success/<int:event_id>', payment_successful, name='payment_successful'),
    path('api/payment-failed/<int:event_id>', payment_failed, name='payment_failed'),
    path('api/', include('paypal.standard.ipn.urls'))
]
