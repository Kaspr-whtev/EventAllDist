# EventAllDist
 Główny folder na aplikację mikroserwisową do zarządzania wydarzeniami. Każdy folder jest osobnym 'projektem'

 ## ApiGateway
 Gateway do aplikacji.
 Aby odpalić wystarczy komenda `docker compose up`. Gateway chodzi na 4 portach: 8000,8001,8443,8444, te muszą pozostać wolne, zatem pozostałe apki muszą chodzić na innych portach.  
 aby dodać nowe przekierowanie należy w pliku `kong.yml`:
 - w aplikacji do której przekierowujemy w `settings.py` dodać `'host.docker.internal'` do ALLOWED_HOSTS
 - w gatewayu dodać nowy route w pliku `kong.yml`
    - name może być dowolne (unikalne)
    - url do strony, localhost zamieniamy na `host.docker.internal`
 - Jako przykład jest zrobiony route do testowej apki django 'testDjango' z tego repo odpalonej na porcie 8010 (aby zostać przekierowanym trzeba wejść na `http://localhost:8000/test`
 - Jako drugi przykład jest przekierowanie do strony zewnętrznej example.com
