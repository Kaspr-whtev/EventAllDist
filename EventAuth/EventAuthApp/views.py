from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from .forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, UntypedToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
import json
from django.urls import reverse
import jwt
from django.views.decorators.csrf import csrf_exempt
import requests
from django.forms.models import model_to_dict


# Create your views here.


def home(request):
    return render(request, 'home.html')


def logout_view(request):
    auth.logout(request)
    response = redirect('/eventauth')
    response.delete_cookie('JWT')

    return response

# @csrf_exempt
# def register(request):
#     print("create user form", request.method)

#     form = CreateUserForm()

#     if request.method == "POST":
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             new_user = form.save()
#             print(model_to_dict(new_user))
#             r = requests.post('http://eventparticipant:8002/api/get_user/', data=model_to_dict(new_user))
#             print(r.status_code)
#             return redirect("my-login")
        
#     context = {'registerform': form}

#     return render(request, 'register.html', context=context)

@csrf_exempt
def register(request):
    print("create user form", request.method)

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            print(model_to_dict(new_user))

            urls = [
                'http://eventparticipant:8002/api/get_user/',
                'http://eventnotification:8004/api/get_user/',
                'http://eventorganizer:8003/api/get_user/'
            ]
            
            data = model_to_dict(new_user)
            for url in urls:
                try:
                    r = requests.post(url, data=data)
                    print(f"Request to {url} returned status code {r.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"Request to {url} failed: {e}")

            return redirect("my-login")
        
    context = {'registerform': form}

    return render(request, 'register.html', context=context)



def my_login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                payload = {
                    'username': user.username,  # Dodaj nazwę użytkownika do payloadu
                    'email': user.email,  # Dodaj email użytkownika do payloadu
                }
                # Zalogowanie się powiodło, generuj token JWT
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                print("Acces token = ", access_token)
                jwt_token = jwt.encode(payload, key='secret', algorithm='HS256')  # Koduj payload do tokena JWT

                auth.login(request, user)

                print("Zawartosc payloadu:", payload)

                
                # Ustawienie ciasteczka JWT
                response = redirect('dashboard')
                response.set_cookie('JWT', jwt_token, httponly=False)  # Ustawienie ciasteczka JWT z dostępem tylko przez HTTP
                
                return response  # Przekierowanie użytkownika do strony głównej lub innej widocznej strony po zalogowaniu
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
    if generated_jwt:
        print(f"JWT token in session: {generated_jwt}")
    return render(request, 'dashboard.html', {'generated_jwt': generated_jwt})


def verify_token(request):
    print("Received request in verify_token")  # Debugowanie
    if request.method == 'POST':
        print("Request method is POST")  # Debugowanie
        try:
            data = json.loads(request.body)
            jwt_token = data.get('jwt_token')
            
            if not jwt_token:
                print("No token in request")  # Debugowanie
                return JsonResponse({'error': 'Token is missing'}, status=400)

            print(f"JWT token: {jwt_token}")  # Debugowanie
            # Weryfikacja tokena JWT
            token = UntypedToken(jwt_token)
            validated_token = JWTAuthentication().get_validated_token(token)
            user = JWTAuthentication().get_user(validated_token)

            # Zwrot danych użytkownika
            return JsonResponse({'username': user.username, 'email': user.email})
        except (TokenError, InvalidToken) as e:
            print(f"Token error: {str(e)}")  # Debugowanie
            return JsonResponse({'error': str(e)}, status=400)
    else:
        print("Invalid request method")  # Debugowanie
        return JsonResponse({'error': 'Invalid request method'}, status=405)

