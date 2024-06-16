from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import EventForm, EventSignupForm, NewUserForm
from .models import Event, Participant
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
import stripe
import time
from EventParticipant.models import UserPayment
from rest_framework_simplejwt.tokens import RefreshToken
import requests
import jwt
from .utils import authenticate_user
from django.contrib.auth.decorators import login_required




def participant_home_page(request):
    return render(request, 'par_home.html', context={"path_show_events": '/participant/api/show-events/'})

def show_events(request):
    authenticated = authenticate_user(request)
    print("auth res = " + str(authenticated))
    if authenticated:
        events = Event.objects.all()
        users = Participant.objects.all()
        return render(request, 'show_events.html', context={'events': events, 'users': users, 'path_par_home': '/participant/api/par_home'})
    else:  
        return render(request, 'par_home.html')


@csrf_exempt
def get_event(request):
    print("create event form", request.method, request.POST)
    if request.method == "POST":
        data = request.POST.dict()
        print(data)
        data["primary"] = data.pop("id", "")
        form = EventForm(data)

        if form.is_valid():
            form.save()
            print(Event.objects.all())

    return JsonResponse(data={})

@csrf_exempt
def get_user(request):
    print("create user form", request.method, request.POST)
    if request.method == "POST":
        data = request.POST.dict()
        # print(data)
        # data["name"] = data.pop("organizer_name", "")
        form = NewUserForm(data)

        if form.is_valid():
            form.save()

    return JsonResponse(data={})


@csrf_exempt
def delete_event(request):
    print("delete ", request.method, request.POST)
    if request.method == "POST":
        data = request.POST.dict()
        print(Event.objects.all())
        event = Event.objects.get(pk=data.get("id"))
        event.delete()

    return JsonResponse(data={})


@csrf_exempt
def edit_event(request):
    print("edit ", request.method, request.POST)
    if request.method == "POST":
        data = request.POST.dict()
        print(Event.objects.all())
        event = Event.objects.get(pk=data.get("id"))
        form = EventForm(request.POST, instance=event)
        form.save()

    return JsonResponse(data={})


def show_event_details(request, event_id):
    # Pobierz obiekt wydarzenia na podstawie przekazanego identyfikatora
    event = get_object_or_404(Event, pk=event_id)
    host = request.get_host()

    participants = event.participants.all()


    # paypal_checkout = {
    #     'business': settings.PAYPAL_RECEIVER_EMAIL,
    #     'amount': Event.ticket_price,
    #     'item_name': Event.name,
    #     'invoice': uuid.uuid4(),
    #     'currency_code': 'USD',
    #     'notify_url': f"http://{host}{reverse('paypal-ipn')}",
    #     'return_url': f"http://{host}{reverse('payment_successful', kwargs = {'event_id': event_id})}",
    #     'cancel_url': f"http://{host}{reverse('payment_failed', kwargs = {'event_id': event_id})}",
    # }

    # paypal_payment_form = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'event': event,
        'participants': participants,
        #'paypal': paypal_payment_form
    }

    # Przekazujesz obiekt wydarzenia do szablonu HTML
    return render(request, 'event_details.html', context)

# def payment_successful(request, event_id):
#     event = Event.objects.get(id=event_id)
#     return render(request, 'payment_success.html', {'event': event})

# def payment_failed(request, event_id):
#     event = Event.objects.get(id=event_id)
#     return render(request, 'payment_failed.html', {'event': event})


def product_page(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	if request.method == 'POST':
		checkout_session = stripe.checkout.Session.create(
			payment_method_types = ['card'],
			line_items = [
				{
					'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': "test_name",
                        },
                        'unit_amount': int(5 * 100),  # Stripe wymaga kwoty w centach
                    },
					'quantity': 1,
				},
			],
			mode = 'payment',
			customer_creation = 'always',
			success_url = settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
			cancel_url = settings.REDIRECT_DOMAIN + '/payment_cancelled',
		)
		return redirect(checkout_session.url, code=303)
	return render(request, 'product_page.html')


def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session_id = request.GET.get('session_id', None)
    
    if checkout_session_id is not None:
        session = stripe.checkout.Session.retrieve(checkout_session_id)
        customer = stripe.Customer.retrieve(session.customer)
        
        
        # user_payment = UserPayment.objects.get(app_user=user_id)
        # user_payment.stripe_checkout_id = checkout_session_id
        # user_payment.save()
        new_payment = UserPayment(payment_bool=True, stripe_checkout_id=checkout_session_id)
        new_payment.save()
        
        return render(request, 'payment_successful.html', {'customer': customer})
    else:
        # Obsłuż przypadek braku session_id
        return render(request, 'payment_failed.html')


def payment_cancelled(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	return render(request, 'payment_cancelled.html')


@csrf_exempt
def stripe_webhook(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	time.sleep(10)
	payload = request.body
	signature_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None
	try:
		event = stripe.Webhook.construct_event(
			payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
		)
	except ValueError as e:
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		return HttpResponse(status=400)
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		session_id = session.get('id', None)
		time.sleep(15)
		user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
		user_payment.payment_bool = True
		user_payment.save()
	return HttpResponse(status=200)


def some_view(request):
    auth_context = authenticate_user(request)
    return render(request, 'some_template.html', context=auth_context)
    # user_authenticated = False
    # # Uzyskanie ciasteczka JWT z żądania
    # jwt_token = request.COOKIES.get('JWT', None)

    # jwt_payload = None
    # error_message = None
    # username = None
    # email = None

    # if jwt_token:
    #     # Dekodowanie zawartości tokena JWT
    #     try:
    #         jwt_payload = jwt.decode(jwt_token, key='secret', algorithms=['HS256'])  
    #         if 'username' in jwt_payload:
    #             username = jwt_payload['username']
    #         if 'email' in jwt_payload:
    #             email = jwt_payload['email']

    #         if username and email:
    #             participant = Participant.objects.filter(username=username, email=email).first()
    #             if participant:
    #                 user_authenticated = True
    #                 user = authenticate(username=username, password=None)  # Password=None, bo nie mamy hasła
    #                 if user is not None:
    #                     login(request, user)

    #     except jwt.ExpiredSignatureError:
    #         error_message = 'Token JWT wygasł.'
    #     except jwt.InvalidTokenError as e:
    #         error_message = f'Nieprawidłowy token JWT: {str(e)}'

    # # Przekazanie danych do szablonu HTML
    # context = {'jwt_payload': jwt_payload, 'jwt_token': jwt_token, 'error_message': error_message, 'username': username, 'email': email, 'user_authenticated': user_authenticated}
    # return render(request, 'some_template.html', context=context)


@csrf_exempt
def event_signup(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            participant, created = Participant.objects.get_or_create(
                email=email,
                defaults={'username': username}
            )
            event.participants.add(participant)

            data = {'email': email, 'username': username, 'id': event_id}
            r = requests.post('http://eventorganizer:8003/api/event_signup/', data=data)
            return redirect('show-events')
    else:
        form = EventSignupForm()
    return render(request, 'event_signup.html', {'form': form, 'event': event})


