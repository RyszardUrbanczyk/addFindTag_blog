from django.urls import reverse
import pytest

from blog_app.models import Program, Post, Gallery, Tag


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
def test_program_list_user_login(client, program, users):
    client.force_login(users[0])
    response = client.get(reverse('program-list'))
    assert response.status_code == 200
    programs_from_view = response.context['objects']
    assert programs_from_view.count() == len(program)
    for x in programs_from_view:
        assert x in program


@pytest.mark.django_db
def test_program_list_user_not_login(client):
    response = client.get(reverse('program-list'))
    assert response.status_code == 200


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
def test_gallery_list_user_not_login(client):
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


@pytest.mark.django_db
def test_add_tag_user_login(client, program, users):
    client.force_login(users[0])
    name = 'tag1'
    program_id = program[0].id
    response = client.post(reverse('add-tag'), {'name': name,
                                                "applications": program_id})

    assert response.status_code == 302
    assert response.url == reverse('program-list')
    Tag.objects.get(name=name, applications=program[0])


@pytest.mark.django_db
def test_add_tag_user_not_login(client):
    response = client.get(reverse('add-tag'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_post_user_login(client, program, users):
    client.force_login(users[0])
    title = 'Post nr 1'
    author_id = users[0].id
    body = 'Treśc posta'
    program_id = program[0].id
    response = client.post(reverse('add-post'), {'title': title, 'author': author_id,
                                                 'body': body, 'programs': program_id})

    assert response.status_code == 302
    assert response.url == reverse('program-list')
    Post.objects.get(title=title, author=users[0], body=body, programs=program[0])


@pytest.mark.django_db
def test_add_post_user_not_login(client):
    response = client.get(reverse('add-post'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_register(client):
    response = client.get(reverse('register'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_post_2_user_login(client, program, users):
    client.force_login(users[0])
    title = 'Post nr 1'
    author_id = users[0].id
    body = 'Treśc posta'
    program_id = program[0].id
    assert Post.objects.all().count() == 0
    client.post(reverse('add-post'), {'title': title, 'author': author_id,
                                      'body': body, 'programs': program_id})

    assert Post.objects.all().count() == 1
    Post.objects.get(title=title, author=users[0], body=body, programs=program[0])
