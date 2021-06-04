from account.models import Friend, Status, Follower, Profile
from account.forms import ProfileForm
# from app.social_network.apps.registration.models import 
from registration.forms import UserRegisterForm

from _pytest.monkeypatch import resolve
import pytest
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from pytest_django.asserts import assertTemplateUsed, assertRedirects


@pytest.fixture
def users():
    users = list()
    test_user1 = User.objects.create_user(username="testuser1", password="12345")
    test_user1.save()
    users.append(test_user1)

    test_user2 = User.objects.create_user(username="testuser2", password="12345")
    test_user2.save()
    users.append(test_user2)

    return users


@pytest.fixture
def Profiles(users):
    test_note1 = Profile.objects.create(user=users[0], city="testuser1")
    test_note2 = Profile.objects.create(user=users[1], city="testuser2")


@pytest.mark.parametrize(
    "url", [r"/login"]
)
def test_response_status(client, url):
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "url, template",
    [        
        (r"/login", r"registration/login.html"),        
    ],
)
def test_right_templates(client, url, template):
    response = client.get(url)

    # assertTemplateUsed(response, template)


def test_redirect_to_login(client):
    response = client.get(r"/")

    assertRedirects(response, r"/registration/login")


@pytest.mark.django_db
def test_index(client, users):
    client.login(username="testuser1", password="12345")

    response = client.get(r"/")
    assertTemplateUsed(response, r"note/notes_list.html")


@pytest.mark.django_db
def test_delete_note(client, notes):
    user = User.objects.first()
    assert client.login(username=user.username, password="12345")

    note = Profile.objects.filter(user=user).first()

    note_amount = Profile.objects.count()
    response = client.get(fr"/{note.pk}/delete")

    assert note_amount - 1 == Profile.objects.count()
    assert not Profile.objects.filter(pk=note.pk)


@pytest.mark.django_db
def test_edit_note(client, notes):
    user = User.objects.first()
    assert client.login(username=user.username, password="12345")

    note = Profile.objects.filter(user=user).first()

    note_amount = Profile.objects.count()
    response = client.get(fr"/{note.pk}/edit")

    assert response.status_code == 200
    assert note_amount == Profile.objects.count()
    assert Profile.objects.filter(pk=note.pk)


@pytest.mark.django_db
def test_signup(client):
    data = {
        "username": "Vasya",
        "email": "vasya@gmail.com",
        "password1": "vasyapassword",
        "password2": "vasyapassword",
    }
    assert UserRegisterForm(data=data).is_valid()

    client.post(r"/posts/post", data)
    assert User.objects.filter(username=data["username"])


@pytest.mark.django_db
def test_add_profile(client, users):
    data = {"title": "test title", "content": "sample content"}
    assert UserRegisterForm(data=data).is_valid()

    profile_count = Profile.objects.count()
    client.login(username=users[0].username, password="12345")
    client.post(r"/registration/login", data)
    assert profile_count + 1 == Profile.objects.count()


@pytest.mark.django_db
def test_change_password(client, users):
    data = {
        "old_password": "12345",
        "new_password1": "hellohihihi",
        "new_password2": "hellohihihi",
    }
    user = users[0]
    assert PasswordChangeForm(user, data=data).is_valid()

    assert client.login(username=user.username, password="12345")
    response = client.post(r"/authentication/change-password", data)
    assert client.login(username=user.username, password=data["new_password2"])
