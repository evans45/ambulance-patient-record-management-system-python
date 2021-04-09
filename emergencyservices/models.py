from django.db import models
from django.urls import reverse

# Create your models here.

class Medic(models.Model):
    hworker = models.CharField(max_length=30)
    loginID = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    institute = models.CharField(max_length=30)
    class Meta:
     managed = False


