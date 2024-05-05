from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from .models import Event
from .serializers import EventSerializer
from rest_framework.response import Response
from .forms import EventForm
from .producer import publish


class EventViewSet(viewsets.ViewSet):
    def list_events(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create_event(self, request):
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('event_created', serializer.data)
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
        publish('event_updated', serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


    def delete_event(self, request, pk=None):
        event = Event.objects.get(id=pk)
        event.delete()
        publish('event_deleted', pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

def create_event_form(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create-event')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})

def organizer_home_page(request):
    return render(request, 'org_home.html')
