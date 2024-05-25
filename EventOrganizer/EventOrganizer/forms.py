from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['date', 'place', 'organizer_name', 'ticket_price', 'name', 'description']
