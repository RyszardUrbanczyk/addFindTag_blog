from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Program(models.Model):
    """
    Model - creating blog topics in the database.
    """
    name = models.CharField(max_length=50)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

    def get_detail_url(self):
        """
        Required for viewing id program.
        """
        return f'/program-detail/{self.id}'


class Tag(models.Model):
    """
    Model - creating tags in the database.
    """
    name = models.CharField(max_length=200)
    applications = models.ManyToManyField(Program)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Model - creating post in the database.
    Relation to the Program model.
    """
    title = models.CharField(max_length=120)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    body_image = models.ImageField(null=True, blank=True, upload_to='images/')
    publish = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    programs = models.ForeignKey(Program, on_delete=models.CASCADE)  # related_name='+'

    # class Meta:
    #     verbose_name_plural = "posts"

    def __str__(self):
        return f'{self.title}'

    def get_detail_url(self):
        """
        Required when creating comments for a id post.
        """
        return f'/add-comment/{self.id}'

    def get_detail_url_2(self):
        """
        Required when we want to edit an post.
        """
        return f'/edit-post/{self.id}'


class Comment(models.Model):
    """
    Model - creating comments in the database.
    Relation to the Post model.
    """
    name = models.CharField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Gallery(models.Model):
    """
    Model - creating galleries in the database.
    """
    name = models.CharField(max_length=50)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_detail_url(self):
        """
        Required when we want to see the gallery.
        """
        return f'/gallery-detail/{self.id}'


class Image(models.Model):
    """
    Model - adding images in the database.
    Relation to the Gallery model.
    """
    name = models.CharField(max_length=200, null=False)
    gallery_image = models.ImageField(null=False, blank=False, upload_to='images/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    galleries = models.ForeignKey(Gallery, on_delete=models.CASCADE, verbose_name='Galerie')
