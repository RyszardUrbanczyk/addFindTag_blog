# Generated by Django 3.1.7 on 2021-03-22 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0003_gallery_imagetogallery'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ImageToGallery',
            new_name='Image',
        ),
    ]
