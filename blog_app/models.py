from django.db import models
from django.contrib.auth.models import User


# Create your models here.


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
    applications = models.ManyToManyField(Program)

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


class Gallery(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_detail_url(self):
        return f'/gallery-detail/{self.id}'


class Image(models.Model):
    name = models.CharField(max_length=200, unique=True, null=False)
    gallery_image = models.ImageField(null=False, blank=True, upload_to='images/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    galleries = models.ForeignKey(Gallery, on_delete=models.CASCADE, verbose_name='Galerie')
