from django.db import models

class Event(models.Model):
    date = models.DateTimeField()
    place = models.CharField(max_length=100)
    organizer_name = models.CharField(max_length=100)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    name = models.CharField(max_length=255, default="")
    description = models.TextField(default="", null=True)


class Organizer(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, default=None, null=True)

    def __str__(self):
        return self.name