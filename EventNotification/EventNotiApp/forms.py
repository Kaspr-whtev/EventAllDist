from django import forms
from .models import UsersToEmail



class NewUserForm(forms.ModelForm):
    class Meta:
        model = UsersToEmail
        fields = ['username', 'email']

