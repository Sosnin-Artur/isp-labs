import pytest
from account.models import Friend, Status, Follower, Profile
from django.contrib.auth.models import User
from django.utils.timezone import now


@pytest.fixture
def user():
    return User.objects.create_user("Vasya", "vasya@gmail.com", "vasyapassword")

@pytest.fixture
def profile(user):
    return Profile.objects.create(user=user, city="Sample")


@pytest.mark.django_db
def test_create_profile(profile):
    assert Profile.objects.count() == 1

@pytest.mark.django_db
def test_profile_type(profile):
    assert isinstance(profile, Profile)

@pytest.mark.django_db
def test_owner(profile, user):
    assert profile.user == user

@pytest.mark.django_db
def test_str(profile):
    assert str(profile.user) == str(profile)
