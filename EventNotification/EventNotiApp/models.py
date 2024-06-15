from django.db import models

class UsersToEmail(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, default=None, null=True)
