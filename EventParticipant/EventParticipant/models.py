from django.db import models


class Event(models.Model):
    date = models.DateTimeField()
    place = models.CharField(max_length=100)
    name = models.CharField(max_length=255, default="")
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
