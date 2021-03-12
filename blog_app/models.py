from django.db import models
from django.contrib.auth.models import User
# from django.utils import timezone

# Create your models here.


class Program(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_detail_url(self):
        return f'/edit_program/{self.id}'


class Tag(models.Model):
    # STATUS_CHOICES = [
    #     ('draft', 'Draft'),
    #     ('published', 'Published')
    # ]

    title = models.CharField(max_length=120)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    uptated = models.DateTimeField(auto_now=True)
    programs = models.ManyToManyField(Program)


