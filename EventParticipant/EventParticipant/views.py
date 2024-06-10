from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import EventForm
from .models import Event
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


def participant_home_page(request):
    return render(request, 'par_home.html', context={"path_show_events": '/participant/api/show-events/'})

def show_events(request):
    events = Event.objects.all()
    return render(request, 'show_events.html', context={'events': events, 'path_par_home': '/participant/api/par_home'})


@csrf_exempt
def get_event(request):
    print("create event form", request.method, request.POST)
    if request.method == "POST":
        data = request.POST.dict()
        print(data)
        # data["name"] = data.pop("organizer_name", "")
        form = EventForm(data)

        if form.is_valid():
            form.save()

    return JsonResponse(data={})

def show_event_details(request, event_id):
    # Pobierz obiekt wydarzenia na podstawie przekazanego identyfikatora
    event = get_object_or_404(Event, pk=event_id)
    host = request.get_host()

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
    # Uzyskanie ciasteczka JWT z żądania
    jwt_token = request.COOKIES.get('JWT', None)

    # Możesz teraz wykorzystać wartość ciasteczka JWT, na przykład:
    jwt_payload = None
    error_message = None
    username = None
    email = None

    if jwt_token:
        # Dekodowanie zawartości tokena JWT
        try:
            jwt_payload = jwt.decode(jwt_token, key='secret', algorithms=['HS256'])  # Dodaj algorytm dekodowania
            # Sprawdź, czy payload zawiera nazwę użytkownika i adres e-mail
            if 'username' in jwt_payload:
                username = jwt_payload['username']
            if 'email' in jwt_payload:
                email = jwt_payload['email']
        except jwt.ExpiredSignatureError:
            error_message = 'Token JWT wygasł.'
        except jwt.InvalidTokenError as e:
            error_message = f'Nieprawidłowy token JWT: {str(e)}'

    # Przekazanie danych do szablonu HTML
    context = {'jwt_payload': jwt_payload, 'jwt_token': jwt_token, 'error_message': error_message, 'username': username, 'email': email}
    return render(request, 'some_template.html', context=context)

