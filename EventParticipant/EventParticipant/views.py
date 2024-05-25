from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .forms import EventForm
from .models import Event
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse

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
        data["name"] = data.pop("organizer_name", "")
        form = EventForm(data)

        if form.is_valid():
            form.save()

    return JsonResponse(data={})

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