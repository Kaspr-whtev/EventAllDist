from django.db import models

class Emails(models.Model):
    email = models.EmailField(unique=True)
