from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    is_club = models.BooleanField(default=False)
    is_dean = models.BooleanField(default=False)


# class Dean(models.Model):
class Request(models.Model):
    title = models.CharField(max_length=255,null=False,blank=False)

    def __str__(self):
        return self.title

    '''def get_absolute_url(self):
        return reversed()'''


class Club(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    requests = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='requests')

    def __str__(self):
        return self.user
