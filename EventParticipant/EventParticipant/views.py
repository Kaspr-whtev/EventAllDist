from django.shortcuts import render

from .models import Event

def participant_home_page(request):
    return render(request, 'par_home.html')

def show_events(request):
    events = Event.objects.all()
    return render(request, 'show_events.html', {'events': events})

