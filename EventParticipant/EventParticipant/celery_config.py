# import os

# from celery import Celery

# from django.conf import settings

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EventParticipant.settings")

# app = Celery("EventParticipant")
# app.config_from_object("django.conf:settings", namespace="CELERY")
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# if __name__ == '__main__':
#     app.start()