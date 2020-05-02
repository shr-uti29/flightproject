from django.db import models

# Create your models here.
class Destination(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField()

class Feedback(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=300)
