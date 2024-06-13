from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, status
from .models import Event
from .serializers import EventSerializer
from rest_framework.response import Response
from .forms import EventForm, DeleteEventForm, EditEventForm
from django.views.decorators.csrf import csrf_exempt
import requests
from django.forms.models import model_to_dict
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
    
    def edit_event_form(self, request, pk=None):
        event = get_object_or_404(Event, id=pk)
        reason_for_edit_form = EditEventForm(request.POST or None)  # Nowa instancja formularza tylko dla powodu edycji
        if request.method == 'POST':
            form = EventForm(request.POST, instance=event)
            if form.is_valid():
                reason_for_edit = reason_for_edit_form['reason_for_edit'].value()  # Pobieramy wartość pola z formularza ReasonForEditForm
                print(f"Successful edit with reason: {reason_for_edit}")
                form.save()
                return redirect('show-events')
        else:
            form = EventForm(instance=event)
        return render(request, 'edit_event.html', {'form': form, 'event': event, 'reason_for_edit_form': reason_for_edit_form})


    
    def delete_event_form(self, request, pk=None):
        event = get_object_or_404(Event, id=pk)
        if request.method == 'POST':
            event.delete()
            return redirect('show-events')
        return redirect('show-events')
    
    def confirm_delete_event(self, request, pk=None):
        event = get_object_or_404(Event, id=pk)
        if request.method == 'POST':
            form = DeleteEventForm(request.POST)
            if form.is_valid():
                reason = form.cleaned_data['reason']
                # Here you can save the reason to the database or perform other actions
                r = requests.post('http://eventparticipant:8002/api/delete_event/', data=model_to_dict(event))
                event.delete()
                # return redirect('show-events')
                return redirect('/organizer/api/show-events/')
        else:
            form = DeleteEventForm()
        return render(request, 'confirm_delete_event.html', context={'form': form, 'event': event, "show_events_path":'/organizer/api/show-events/'})






@csrf_exempt
def create_event_form(request):
    print("create event form", request.method)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            new_event = form.save()
            print(model_to_dict(new_event))
            r = requests.post('http://eventparticipant:8002/api/get_event/', data=model_to_dict(new_event))
            print(r.status_code)

            return redirect('/organizer/api/create/')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})


def organizer_home_page(request):
    return render(request, 'org_home.html', context={"path": '/organizer/api/create/', "path_show_events": '/organizer/api/show-events/'})

def show_events(request):
    events = Event.objects.all()
    return render(request, 'show_events.html', context={'events': events, 'path_org_home': '/organizer/api/org_home'})