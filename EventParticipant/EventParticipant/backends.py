from django.contrib.auth.backends import BaseBackend
from .models import Participant

class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, email=None):
        try:
            participant = Participant.objects.get(username=username, email=email)
            return participant
        except Participant.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Participant.objects.get(pk=user_id)
        except Participant.DoesNotExist:
            return None
