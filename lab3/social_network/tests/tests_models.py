import pytest
from account.models import Friend, Status, Follower, Profile
from dialogs.models import Message
from posts.models import Post, Like, Comment

from django.contrib.auth.models import User
from django.utils.timezone import now


@pytest.fixture
def user():
    return User.objects.create_user("Vasya", "vasya@gmail.com", "vasyapassword")

@pytest.fixture
def user2():
    return User.objects.create_user("Anatoliy", "anatol@gmail.com", "vasyapassword")

@pytest.fixture
def profile():
    return {"gender": "M", "user": user(), "city": "Minsk"}

@pytest.fixture
def post():
    return Post.objects.create(sender=user(), reciever=user2(), message_text="text")

@pytest.fixture
def message():
    return Message.objects.create(author=user(), post_title="title", post_text="text")

@pytest.fixture
def status():
    return Status.objects.create(user=user())

@pytest.fixture
def friend():
    return Friend.objects.create(user=user(), users_friend=user2())

@pytest.fixture
def follower():
    return Follower.objects.create(user=user(), follower_for=user2())

@pytest.fixture
def like():
    return Like.objects.create(user=user(), for_post=post())

@pytest.fixture
def comment():
    return Comment.objects.create(comment_author=user(), post=post())

@pytest.mark.django_db
def test_create_post(post):
    assert Post.objects.count() == 1

@pytest.mark.django_db
def test_create_user(user):
    assert User.objects.count() == 1

@pytest.mark.django_db
def test_create_like(user):
    assert Like.objects.count() == 1

@pytest.mark.django_db
def test_create_comment(user):
    assert Comment.objects.count() == 1

@pytest.mark.django_db
def test_create_profile(user):
    assert Profile.objects.count() == 1

@pytest.mark.django_db
def test_create_friend(user):
    assert Friend.objects.count() == 1

@pytest.mark.django_db
def test_create_status(user):
    assert Status.objects.count() == 1

@pytest.mark.django_db
def test_create_Message(user):
    assert Message.objects.count() == 1

@pytest.mark.django_db
def test_create_follower(user):
    assert Follower.objects.count() == 1

@pytest.mark.django_db
def test_post_type(post):
    assert isinstance(post, Post)

@pytest.mark.django_db
def test_user_type(user):
    assert isinstance(user, User)

@pytest.mark.django_db
def test_frined_type(val):
    assert isinstance(val, Friend)

@pytest.mark.django_db
def test_follower_type(val):
    assert isinstance(val, Follower)

@pytest.mark.django_db
def test_status_type(val):
    assert isinstance(val, Status)

@pytest.mark.django_db
def test_message_type(val):
    assert isinstance(val, message)

@pytest.mark.django_db
def test_like_type(val):
    assert isinstance(val, like)

@pytest.mark.django_db
def test_comment_type(val):
    assert isinstance(val, Comment)

@pytest.mark.django_db
def test_profile_type(val):
    assert isinstance(val, Profile)

@pytest.mark.django_db
def test_owner_post(post, user):
    assert post.author == user

@pytest.mark.django_db
def test_profile(profile, user, post):
    assert profile.user == user
    assert post.author == profile.user

@pytest.mark.django_db
def test_str(post):
    assert post.title == str(post)

@pytest.mark.django_db
def test_account_str(profile, user):
    assert str(profile) == str(user)
