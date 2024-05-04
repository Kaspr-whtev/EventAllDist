from django.db import models


class Event(models.Model):
    date = models.DateTimeField()
    place = models.CharField(max_length=100)
    name = models.CharField(max_length=255, default="")
