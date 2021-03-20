from django.db import models
from django.contrib.auth.models import User
# from django.utils import timezone
from datetime import timezone


# from django.utils import timezone

# Create your models here.



# verbose_name='Nazwa kategorii'

class Program(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.name}'

    def get_detail_url(self):
        return f'/program-detail/{self.id}'


class Tag(models.Model):
    name = models.CharField(max_length=200)
    aplications = models.ManyToManyField(Program)

    def __str__(self):
        return self.name


class Post(models.Model):
    # STATUS_CHOICES = [
    #     ('draft', 'Draft'),
    #     ('published', 'Published')
    # ]

    title = models.CharField(max_length=120)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    body_image = models.ImageField(null=True, blank=True, upload_to='images/')
    publish = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    programs = models.ForeignKey(Program, on_delete=models.CASCADE)  # related_name='+'

    def __str__(self):
        return f'{self.title}'

    def get_detail_url(self):
        return f'/add-comment/{self.id}'


class Comment(models.Model):
    name = models.CharField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
