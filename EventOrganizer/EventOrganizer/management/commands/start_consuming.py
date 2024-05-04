
from django.core.management.base import BaseCommand

from EventOrganizer.consumer import Consumer


class Command(BaseCommand):
    help = 'Launches Listener for user_created message : RabbitMQ'

    def handle(self, *args, **options):
        td = Consumer()
        td.start()
