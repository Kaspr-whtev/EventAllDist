from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import EventForm
from .models import Event

def participant_home_page(request):
    return render(request, 'par_home.html', context={"path_show_events": '/participant/api/show-events/'})

def show_events(request):
    events = Event.objects.all()
    return render(request, 'show_events.html', context={'events': events, 'path_par_home': '/participant/api/par_home'})


@csrf_exempt
def get_event(request):
    print("create event form", request.method, request.POST)
    if request.method == 'POST':
        data = request.POST.dict()
        print(data)
        data["name"] = data.pop("organizer_name", "")
        form = EventForm(data)

        if form.is_valid():
            form.save()

    return JsonResponse(data={})

