from django import forms
from .models import Event, Participant



class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['date', 'place', 'name']


class EventSignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()

class NewUserForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['username', 'email']

