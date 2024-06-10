from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save


class Event(models.Model):
    date = models.DateTimeField()
    place = models.CharField(max_length=100)
    name = models.CharField(max_length=255, default="")
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

class UserPayment(models.Model):
    #app_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)


class Participant(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, default=None, null=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_payment(sender, instance, created, **kwargs):
    if created:
        UserPayment.objects.create(app_user = instance)

