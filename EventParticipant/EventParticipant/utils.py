import jwt
from django.contrib.auth import authenticate, login
from .models import Participant
from .backends import CustomBackend

# def authenticate_user(request):
#     user_authenticated = False
#     jwt_token = request.COOKIES.get('JWT', None)

#     jwt_payload = None
#     error_message = None
#     username = None
#     email = None
#     participant = None

#     if jwt_token:
#         print("token good")
#         try:
#             jwt_payload = jwt.decode(jwt_token, key='secret', algorithms=['HS256'])
#             if 'username' in jwt_payload:
#                 username = jwt_payload['username']
#             if 'email' in jwt_payload:
#                 email = jwt_payload['email']

#             if username and email:
#                 print("username and email good")
#                 participant = Participant.objects.filter(username=username, email=email).first()
#                 if participant:
#                     print("participant good")
#                     #user_authenticated = True
#                     user = authenticate(request, username=username, password=None)  # Password=None, bo nie mamy hasła
#                     print("participant = " + str(participant.username))
#                     print ("user = " + str(user))
#                     if user is not None:
#                         login(request, user)
#                         user_authenticated = True
#                         print("user authenticated")
#                         #return True
#                     else: print ("user is NONE")

#         except jwt.ExpiredSignatureError:
#             error_message = 'Token JWT wygasł.'
#         except jwt.InvalidTokenError as e:
#             error_message = f'Nieprawidłowy token JWT: {str(e)}'

#     print("user NOT authenticated")
#     #return False

#     return {
#         'jwt_payload': jwt_payload,
#         'jwt_token': jwt_token,
#         'error_message': error_message,
#         'username': username,
#         'email': email,
#         'user_authenticated': user_authenticated,
#         'participant': participant
#     }


def authenticate_user(request):
    user_authenticated = False
    jwt_token = request.COOKIES.get('JWT', None)

    jwt_payload = None
    error_message = None
    username = None
    email = None
    participant = None

    if jwt_token:
        try:
            jwt_payload = jwt.decode(jwt_token, key='secret', algorithms=['HS256'])
            if 'username' in jwt_payload:
                username = jwt_payload['username']
            if 'email' in jwt_payload:
                email = jwt_payload['email']

            if username and email:
                custom_backend = CustomBackend()
                participant = custom_backend.authenticate(request, username=username, email=email)
                print("user = " + str(participant))
                if participant is not None:
                    print("user authenticated")
                    # Ustawienie użytkownika w sesji (można też użyć request.user)
                    request.session['participant_id'] = participant.id
                    user_authenticated = True
                    return True

        except jwt.ExpiredSignatureError:
            error_message = 'Token JWT wygasł.'
        except jwt.InvalidTokenError as e:
            error_message = f'Nieprawidłowy token JWT: {str(e)}'

    return False
    # return {
    #     'jwt_payload': jwt_payload,
    #     'jwt_token': jwt_token,
    #     'error_message': error_message,
    #     'username': username,
    #     'email': email,
    #     'user_authenticated': user_authenticated,
    #     'participant': participant
    # }
