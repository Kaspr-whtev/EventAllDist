# EventAllDist
 Główny folder na aplikację mikroserwisową do zarządzania wydarzeniami. Każdy folder jest osobnym 'projektem'

 ## Uruchamianie
 aplikację można odpalic komentda `docker-compose up` z głównego folderu (EventAllDist), komenda ta odpala gateway i mikroserwisy participanta i organizera.
 W przypadku zmian w kodzie, lepiej jest odpalić komendą `docker-compose up --build` aby mieć pewność że zmiany zostaną wprowadzone.

 ## Kolejne mikroserwisy
 aby dodac kolejne mikroserwisy należy:
 1. dodać do głównego pliku `docker-compose.yml` nowy service, przykład:
 ```
  eventparticipant:
    build:
      context: EventParticipant
      dockerfile: DockerFile
    command: python manage.py runserver 0.0.0.0:8002
    ports:
      - "8002:8002" 
 ```
 2. stworzyć plik DockerFile wewnątrz mikroserwisu, przykład:
 ```
FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /EventParticipant
COPY requirements.txt /EventParticipant/requirements.txt
RUN pip install -r requirements.txt
COPY . /EventParticipant

 ```
 3. dodać do pliku `kong.yml` w głównym folderze nową ścieżkę, przykład:
```
  - name: participant
    url: http://host.docker.internal:8002/
    routes:
      - name: participant-route
        paths:
          - /participant
```
UWAGA: jeśli korzystasz z api gateway (pk. 3 powyżej) i jeśli masz przekierowania wewnątrz mikroserwisu, należy podawać linki w sposób absolutny z prefiksem nadanym w `kong.yml`, przykład z EventParticipant:
- Zmienna podawana do html'a z prefiksem nadanym w kong.yml (/participant/):
```
#views.py

def participant_home_page(request):
    return render(request, 'par_home.html', context={"path_show_events": '/participant/api/show-events/'})
```
- Wykorzystanie do przechodzenia między linkami:
```
<!--par_home.html-->

<a href={{path_show_events}}>Show Events</a>
```

## Komunikowanie się mikroserwisów
Mikroserwisy komunikują się między sobą za pomocą http requestów, do tego jest potrzebna biblioteka `requests`.
Przykład wysyłania posta z organizera do participanta o stworzeniu wydarzenia:
### EventOrganizer
- `requests.post` wysyła wiadomość do participanta, podawany tutaj link: `http://127.0.0.1:8002/api/get_event/`, jest bezpośredni (nie idzie przez gateway, stąd port ma taki nr na jakim chodzi serwis i nie ma prefiksu od gatewaya):
```
#views.py

import requests

...

def create_event_form(request):
    print("create event form", request.method)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()

            r = requests.post('http://127.0.0.1:8002/api/get_event/', data=request.POST)
            print(r.status_code)

            return redirect('/organizer/api/create/')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})
```

### EventParticipant
- powstał nowy pattern do odbierania requestów:
```
#urls.py

path('api/get_event/', get_event, name='get_event'),
```
- powstał form do odbierania i sprawdzania danych przychodzących:
```
# forms.py

from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['date', 'place', 'name']

```
- zapis so bazy danych:
```
views.py

def get_event(request):
    print("create event form", request.method, request.POST)
    if request.method == 'POST':
        data = request.POST.dict()
        print(data)
        data["name"] = data.pop("organizer_name", "")
        form = EventForm(data)

        if form.is_valid():
            form.save()

    return JsonResponse(data={})
```

## Elementy które można usunąć
Póki co zostały, jeśli się okaże że musimy coś zmienić:
- cały folder ApiGateway
- cały folder management w EventOrganizer
- `celery_config.py` w EventOrganizer
- `producer.py` w EventOrganizer
- `consumer.py` w EventOrganizer
- wzmianki w `settings.py` w EventOrganizer o: celery, rabbitmq
- `tasks.py` w EventOrganizer
- wyczyścić `requirements.txt` w EventOrganizer
- cały folder management w EventParticipant
- `celery_config.py` w EventParticipant
- `consumer.py` w EventParticipant
- wzmianki w `settings.py` w EventParticipant o: celery, rabbitmq
- `tasks.py` w EventParticipant
- `docker-compose.yml` w EventParticipant
- wyczyścić `requirements.txt` w EventParticipant
- cały folder testDjango

 ## ApiGateway
 folder apigateway jako taki nie jest juz potrzebny
~~Gateway do aplikacji.~~
 ~~Aby odpalić wystarczy komenda `docker compose up`. Gateway chodzi na 4 portach: 8000,8001,8443,8444, te muszą pozostać wolne, zatem pozostałe apki muszą chodzić na innych portach.~~  
 ~~aby dodać nowe przekierowanie należy w pliku `kong.yml`:~~
 ~~- w aplikacji do której przekierowujemy w `settings.py` dodać `'host.docker.internal'` do ALLOWED_HOSTS~~
 ~~- w gatewayu dodać nowy route w pliku `kong.yml`~~
    ~~- name może być dowolne (unikalne)~~
    ~~- url do strony, localhost zamieniamy na `host.docker.internal`~~
 ~~- Jako przykład jest zrobiony route do testowej apki django 'testDjango' z tego repo odpalonej na porcie 8010 (aby zostać przekierowanym trzeba wejść na `http://localhost:8000/test`~~
 ~~- Jako drugi przykład jest przekierowanie do strony zewnętrznej example.com~~
