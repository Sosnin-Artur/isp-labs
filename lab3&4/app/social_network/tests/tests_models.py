import pytest
from account.models import Friend, Status, Follower, Profile, create_user_profile, save_user_profile
from dialogs.models import Message
from posts.models import Post, Like, Comment

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

@pytest.mark.django_db
def test_create_post(user):
    Post.objects.create(author=user, post_time='2020-09-22 23:34:22');
    assert Post.objects.count() == 1

@pytest.mark.django_db
def test_create_user():
    User.objects.create();
    assert User.objects.count() == 1

@pytest.mark.django_db
def test_create_like(user, post):    
    Like.objects.create(user=user, for_post=post, like_or_dislike='LIKE');
    assert Like.objects.count() == 1

@pytest.mark.django_db
def test_create_comment(post, user):    
    Comment.objects.create(post=post, comment_author=user, comment_text="text", comment_pubdate=dt.datetime.now());
    assert Comment.objects.count() == 1
@pytest.mark.django_db
def test_create_friend(user, user2):    
    Friend.objects.create(user=user, users_friend=user2);
    assert Friend.objects.count() == 1

@pytest.mark.django_db
def test_create_status(user):   
    Status.objects.create(user=user);
    assert Status.objects.count() == 1

@pytest.mark.django_db
def test_create_Message(user, user2):
    Message.objects.create(sender=user, reciever=user2, message_text='text', message_time=dt.datetime.now())
    assert Message.objects.count() == 1

@pytest.mark.django_db
def test_create_follower(user, user2):
    Follower.objects.create(user=user, follower_for=user2)
    assert Follower.objects.count() == 1

@pytest.mark.django_db
def test_post_type(post):
    assert isinstance(post, Post)

@pytest.mark.django_db
def test_user_type(user):
    assert isinstance(user, User)

@pytest.mark.django_db
def test_post_str(post):
    assert post.post_title == str(post)

