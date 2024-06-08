from django import forms
from .models import Event

class EventForm(forms.ModelForm):    
    class Meta:
        model = Event
        fields = ['date', 'place', 'organizer_name', 'ticket_price', 'name', 'description']


class DeleteEventForm(forms.Form):
    reason = forms.CharField(label='Reason for deletion', max_length=500, widget=forms.Textarea)

class EditEventForm(forms.Form):
    reason_for_edit = forms.CharField(label='Reason for Edit', max_length=500, required=False, widget=forms.Textarea)


