from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import UsersToEmail
from django.views.decorators.csrf import csrf_exempt
from .forms import NewUserForm
from django.http import HttpResponse, JsonResponse


def home(request):
    if request.method == "POST":
        subject = request.POST.get('subject')
        msg = request.POST.get('message')
        recipient_list = list(get_all_user_emails())
        send_mail(subject, msg, '256511@student.pwr.edu.pl', recipient_list)
        return HttpResponse('email sent successfully')

    return render(request, 'email_home.html')


def get_all_user_emails():
    return UsersToEmail.objects.values_list('email', flat=True)

def show_users(request):
    users = UsersToEmail.objects.all()
    return render(request, 'show_users.html', context={'users': users, 'path_noti_home': '/eventnoti'})


@csrf_exempt
def edit_event(request):
    print("participants from organizer: ", request.method, request.POST)


@csrf_exempt
def get_user(request):
    print("create user form", request.method, request.POST)
    if request.method == "POST":
        data = request.POST.dict()
        print(data)
        # data["name"] = data.pop("organizer_name", "")
        form = NewUserForm(data)

        if form.is_valid():
            form.save()

    return JsonResponse(data={})
