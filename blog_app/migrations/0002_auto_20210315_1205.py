# Generated by Django 3.1.7 on 2021-03-15 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='tags',
            new_name='progrms',
        ),
    ]