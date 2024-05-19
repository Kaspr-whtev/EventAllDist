from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from .models import Event
from .serializers import EventSerializer
from rest_framework.response import Response
from .forms import EventForm
from django.views.decorators.csrf import csrf_exempt
import requests
#from .producer import send_message
# from .tasks import add


class EventViewSet(viewsets.ViewSet):
    def list_events(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create_event(self, request):
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print('created')
        # r = requests.get('https://httpbin.org/basic-auth/user/pass')
        # r.status_code
        #
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_event(self, request, pk=None):
        event = Event.objects.get(id=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def update_event(self, request, pk=None):
        event = Event.objects.get(id=pk)
        serializer = EventSerializer(instance=event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


    def delete_event(self, request, pk=None):
        event = Event.objects.get(id=pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def create_event_form(request):
    print("create event form", request.method)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            print(Event.objects.all())

            r = requests.post('http://eventparticipant:8002/api/get_event/', data=request.POST)
            print(r.status_code)

            return redirect('/organizer/api/create/')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})


def organizer_home_page(request):
    return render(request, 'org_home.html', context={"path": '/organizer/api/create/'})
