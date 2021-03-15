from django.db import models
from django.contrib.auth.models import User


# from django.utils import timezone

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=200)

class Program(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f'{self.name}'

    def get_detail_url(self):
        return f'/program-detail/{self.id}'


class Post(models.Model):
    # STATUS_CHOICES = [
    #     ('draft', 'Draft'),
    #     ('published', 'Published')
    # ]

    title = models.CharField(max_length=120)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    programs = models.ManyToManyField(Program)  # related_name='+'
