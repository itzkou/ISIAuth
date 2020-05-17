import datetime

import django
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    is_club = models.BooleanField(default=False)
    is_dean = models.BooleanField(default=False)


# class Dean(models.Model):
class Request(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests', null=True)
    date = models.DateField(null=False, blank=False, default=django.utils.timezone.now)
    hour = models.TimeField(null=False, blank=False)
    needs = models.CharField(max_length=200)
    domain = models.TextField(max_length=200)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    status = models.BooleanField(default=False)

    # TODO club signature & dean signature (numerique)

    def __str__(self):
        return self.title

    # TODO
    '''def get_absolute_url(self):
        return reversed()'''


class Club(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user
