from django.test import TestCase
from django.urls import reverse, get_resolver
import pytest
from django.utils.encoding import iri_to_uri

from blog_app.models import Program, Post, Gallery


# Create your tests here.

def test_check_index(client):
    response = client.get(reverse('index'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_program_user_login(client, users):
    client.force_login(users[0])
    response = client.get(reverse('program-list'))
    assert response.status_code == 200
    name = 'inDesign'
    description = 'Skład gazet'
    assert Program.objects.all().count() == 0
    client.post(reverse("add-program"), {'name': name,
                                         "description": description})
    assert Program.objects.all().count() == 1
    Program.objects.get(name=name, description=description)


@pytest.mark.django_db
def test_program_list_user_login(client, programs, users):
    client.force_login(users[0])
    response = client.get(reverse('program-list'))
    assert response.status_code == 200
    programs_from_view = response.context['objects']
    assert programs_from_view.count() == len(programs)
    for x in programs_from_view:
        assert x in programs


@pytest.mark.django_db
def test_program_list_user_not_login(client):
    response = client.get(reverse('program-list'))
    assert response.status_code == 200
    # path = response.url.split('?')[0]
    # next = response.url.split('?')[1]
    # assert path == reverse('login')
    # assert next == 'next=/program-list/'


@pytest.mark.django_db
def test_add_gallery_user_login(client, users):
    client.force_login(users[0])
    response = client.get(reverse('add-gallery'))
    assert response.status_code == 200
    name = 'Photoshop'
    description = 'galeria z obrazkami'
    assert Program.objects.all().count() == 0
    client.post(reverse("add-gallery"), {'name': name,
                                         "description": description})
    assert Gallery.objects.all().count() == 1
    Gallery.objects.get(name=name, description=description)


@pytest.mark.django_db
def test_program_list_user_not_login(client):
    response = client.get(reverse('add-gallery'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_gallery_list_user_login(client, galleries, users):
    client.force_login(users[0])
    response = client.get(reverse('gallery-list'))
    assert response.status_code == 200
    galleries_from_view = response.context['objects']
    assert galleries_from_view.count() == len(galleries)
    for x in galleries_from_view:
        assert x in galleries


# Nie działa
# Musi być przesłany id? Jeśli tak jak się to robi?
@pytest.mark.django_db
def test_gallery_detail_user_not_login(client):
    response = client.get(reverse('gallery-detail/%[id]s/'))
    assert response.status_code == 302


