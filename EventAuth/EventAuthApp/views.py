from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from .forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, 'home.html')


def logout_view(request):
    auth.logout(request)
    return redirect('/')


def register(request):

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("my-login")
        
    context = {'registerform': form}

    return render(request, 'register.html', context=context)


def my_login(request):

    form = LoginForm()
    
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")

    context = {'loginform': form}

    return render(request, 'my-login.html', context=context)

@login_required(login_url="my-login")
def dashboard(request):
    return render(request, 'dashboard.html')
