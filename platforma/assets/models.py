from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.sessions.models import Session


class Instrument(models.Model):
    name = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=15, decimal_places=2)

class SessionProfile(models.Model):
    user_id = models.IntegerField()
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.CharField(max_length=20)
    last_accessed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.session_key