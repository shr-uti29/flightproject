from django.db import models
from django.contrib.auth.models import User

#Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Contact = models.CharField(max_length=20,null=False,blank=False)
    Address = models.CharField(max_length=100,null=False,blank=False)
    DOB = models.DateField()
    Gender = models.CharField(max_length=10,null=False,blank=False)

    def __str__(self):
        return "{0}".format(self.user.username)

class Flight(models.Model):
    FlightNo=models.CharField(max_length=10)
    Departure=models.TimeField()
    Arrival=models.TimeField()
    Date=models.DateField()
    From=models.CharField(max_length=25)
    To=models.CharField(max_length=25)

class Flightseat(models.Model):
    seat=models.CharField(max_length=20)
    svalue=models.BooleanField(default=False)
