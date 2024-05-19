from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import Emails


def home(request):
    if request.method == "POST":
        subject = request.POST.get('subject')
        msg = request.POST.get('message')
        recipient_list = list(get_all_user_emails())
        send_mail(subject, msg, '256511@student.pwr.edu.pl', recipient_list)
        return HttpResponse('email sent successfully')

    return render(request, 'email_home.html')


def get_all_user_emails():
    return Emails.objects.values_list('email', flat=True)
