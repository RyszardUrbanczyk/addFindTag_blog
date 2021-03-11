from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Program(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()