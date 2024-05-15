from django.shortcuts import render, get_object_or_404
from .models import Event
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse

def participant_home_page(request):
    return render(request, 'par_home.html')

def show_events(request):
    events = Event.objects.all()
    return render(request, 'show_events.html', {'events': events})

def show_event_details(request, event_id):
    # Pobierz obiekt wydarzenia na podstawie przekazanego identyfikatora
    event = get_object_or_404(Event, pk=event_id)
    host = request.get_host()

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': Event.ticket_price,
        'item_name': Event.name,
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('payment_successful', kwargs = {'event_id': event_id})}",
        'cancel_url': f"http://{host}{reverse('payment_failed', kwargs = {'event_id': event_id})}",
    }

    paypal_payment_form = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'event': event,
        'paypal': paypal_payment_form
    }

    # Przekazujesz obiekt wydarzenia do szablonu HTML
    return render(request, 'event_details.html', context)

def payment_successful(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'payment_success.html', {'event': event})

def payment_failed(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'payment_failed.html', {'event': event})