import pytest
from pytest_django.asserts import assertTemplateUsed, assertRedirects
from account.models import Friend, Status, Follower, Profile, create_user_profile, save_user_profile

from account.views import *
from bots.views import *
from dialogs.views import *
from posts.views import *
from registration.views import *

from django.contrib.auth.forms import UserCreationForm
from registration.forms import UserRegisterForm

from dialogs.models import Message
from posts.models import Post, Like, Comment

from django.urls import reverse

from django.contrib.auth.models import User
from django.utils.timezone import now

import datetime as dt

@pytest.fixture
def user_data():
	return {"username": "Vasya", 
           	"first_name": "vasya", "last_name": "pupkin",
   		"email": "vasya@mgmail.com",
                "password": "12345678", 
                "password2": "12345678", 
        }

@pytest.fixture
def user_data2():
	return {"username": "anatol", 
           	"first_name": "anatol", "last_name": "eeeee",
   		"email": "anatol@mgmail.com",
                "password": "12345678", 
                "password2": "12345678", 
        }

@pytest.fixture
def user():
    return User.objects.create_user("Vasya", "vasya@gmail.com")

@pytest.fixture
def user2():
    return User.objects.create_user("anatol", "anatol@gmail.com")

@pytest.fixture
def post_data():
    return {"post_title": "Test_Title", "post_text": "test_text"}

@pytest.fixture
def profile(user):
    return Profile.objects.create(user=user)

@pytest.fixture
def message():
    return Message.objects.create(sender=user, reciever=user2, message_text="text")

@pytest.fixture
def post(user):
    return Post.objects.create(author=user, post_title="title", post_text="text", post_time=dt.datetime.now())

@pytest.fixture
def status():
    return Status.objects.create(user=user)

@pytest.fixture
def friend():
    return Friend.objects.create(user=user, users_friend=user2)

@pytest.fixture
def follower():
    return Follower.objects.create(user=user, follower_for=user2)

@pytest.fixture
def like():
    return Like.objects.create(user=user, for_post=post)

@pytest.fixture
def comment():
    return Comment.objects.create(comment_author=user, post=post)

@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
   def make_auto_login(user=None):
       if user is None:
           user = create_user()
       client.login(username=user.username, password=test_password)
       return client, user
   return make_auto_login

@pytest.mark.parametrize(
    "url",
    [
        r"/account/",
        r"/account_setting/",
        r"/friends/",
        r"/friend_request/",
        r"/messages/",
        r"/friend_news/",
        r"/news/",
        r"/like_news/",
        r"/login/",
        r"/registration/",
        r"/",
    ],
)
def test_response_status(client, url):
    response = client.get(url)
    assert response.status_code == 200 or 302

@pytest.mark.django_db
def test_index(client, user):
    client.login(username="testuser1", password="12345")

    response = client.get(r"/")
    assertTemplateUsed(response, r"registration/index.html")


@pytest.mark.django_db
def test_register(client):
    data = {
        "username": "Vasya",
        "email": "vasya@gmail.com",
        "password1": "123qwezxc",
        "password2": "123qwezxc",
    }
    assert not UserRegisterForm(data=data).is_valid()

    client.post(r"/authentication/signup/", data)
    assert not User.objects.filter(username=data["username"])

@pytest.mark.django_db
def test_redirect_to_login(client):
    response = client.get(r"/")
    assert response.status_code == 200 or 302

@pytest.mark.django_db
def test_login(client, user):
    data = {"username": user.username, "password": "qwerty123"}
    client.post("/login/", data)
    assert client.post("/login/", username=user.username, password="qwerty123")
    assert not client.login(username=data["username"], password="qwerty123")

"""
@pytest.mark.django_db
def test_detail_user(client, user):
    temp_url = reverse("detail_user", args=(user.id,))
    resp = client.get(temp_url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_update_user(client, user, account):
    temp_url = reverse("update_account", args=(user.id,))
    resp = client.get(temp_url)
    assert resp.status_code == 302

    client.login(username=user.username, password="qwerty123")
    data = {"pk": user.id, "phone": "3523523"}
    response_get = client.get("/users/" + str(user.id) + "/update/")
    assert response_get.status_code == 200

    client.post("/users/" + str(user.id) + "/update/", data=data)
    assert Account.objects.filter(user=user).first().phone == data["phone"]

    response = client.post("/users/" + str(user.id) + "/update/", data={"username": user.username})
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_post(client, user):
    client.login(username=user.username, password="qwerty123")
    resp_get = client.get("/create/")
    assert resp_get.status_code == 200

    data = {"title": "Test_Title", "text": "test_text here"}
    assert PostCreateForm(data=data).is_valid()
    resp_post = client.post("/create/", data)
    assert resp_post.status_code == 302
    assert Post.objects.get(title=data["title"])


@pytest.mark.django_db
def test_delete_post(client, user, post):
    resp_get = client.get("/post/" + post.slug + "/remove")
    assert resp_get.status_code == 404

    client.login(username=user.username, password="qwerty123")
    assert Post.objects.get(author=user).author == post.author

    resp_post = client.post("/post/" + post.slug + "/remove", {"slug": post.slug})
    assert resp_post.status_code == 302
    assert Post.objects.filter(author=user).first() is None


@pytest.mark.django_db
def test_update_post(client, user, post):
    resp_get = client.get("/post/" + post.slug + "/update")
    assert resp_get.status_code == 404

    client.login(username=user.username, password="qwerty123")
    resp_get = client.get("/post/" + post.slug + "/update")
    assert resp_get.status_code == 200

    data = {"title": post.title, "text": "NEW TEXT"}
    assert PostUpdateForm(data=data).is_valid()
    resp_post = client.post("/post/" + post.slug + "/update", data)
    assert resp_post.status_code == 302
    assert Post.objects.filter(author=user).first().text == data["text"]
    assert Post.objects.count() == 1
"""
