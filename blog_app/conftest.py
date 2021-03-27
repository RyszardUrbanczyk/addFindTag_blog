import pytest
from django.test import Client
from blog_app.models import Program, Tag, Post, Comment, Gallery, Image
from django.contrib.auth.models import User


@pytest.fixture
def client():
    c = Client()
    return c


@pytest.fixture
def program():
    program = []
    for x in range(10):
        u = Program.objects.create(name=str(x), description='fajny program')
        program.append(u)
    return program


@pytest.fixture
def users():
    users = []
    for x in range(1, 11):
        u = User.objects.create(username=str(x))
        users.append(u)
    return users


@pytest.fixture
def galleries():
    galleries = []
    for x in range(10):
        g = Gallery.objects.create(name=str(x), description='fajne')
        galleries.append(g)
    return galleries



@pytest.fixture
def tags():
    tags = []
    for x in range(10):
        u = Tag.objects.create(name=str(x))
        tags.append(u)
    return tags