from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from .forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

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


from django.shortcuts import redirect

def my_login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Zalogowanie się powiodło, generuj token JWT
                refresh = RefreshToken.for_user(user)
                auth.login(request, user)
                request.session['jwt_token'] = str(refresh.access_token)  # Zapisz token JWT w sesji
                return redirect('dashboard')
            else:
                # Zalogowanie się nie powiodło
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
    else:
        form = LoginForm()

    context = {'loginform': form}
    return render(request, 'my-login.html', context=context)


@login_required(login_url="my-login")
def dashboard(request):
    generated_jwt = request.session.get('jwt_token')  # Pobierz token JWT z sesji
    return render(request, 'dashboard.html', {'generated_jwt': generated_jwt})
