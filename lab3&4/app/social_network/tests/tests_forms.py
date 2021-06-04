import pytest

from account.models import Friend, Status, Follower, Profile
from account.forms import ProfileForm
# from app.social_network.apps.registration.models import 
from registration.forms import UserRegisterForm
from django.contrib.auth.models import User
from django.utils.timezone import now

@pytest.fixture
def profile_data(user):
    return {"user": user, "city": "city"}

@pytest.fixture
def friend_data(user):
    return {"user": user}

@pytest.fixture
def status_data(user):
    return {"user": user}

@pytest.fixture
def follower_data(user):
    return {"user": user}

@pytest.fixture
def user_data():
    return {"username": "Vasya", "email": "vasya@gmail.com", "password1": "vasyapassword", "password2": "vasyapassword"}

@pytest.fixture
def user():
    return User.objects.create_user("Vasya", "vasya@gmail.com", "vasyapassword")

@pytest.fixture
def friend(profile_data):
    return Friend.objects.create(**profile_data)

@pytest.fixture
def status(profile_data):
    return Status.objects.create(**profile_data)

@pytest.fixture
def profile(profile_data):
    return Profile.objects.create(**profile_data)

@pytest.fixture
def follower(profile_data):
    return Follower.objects.create(**profile_data)

@pytest.fixture
def profile_form(profile_data):
    return ProfileForm(data=profile_data)

@pytest.fixture
def signup_form(user_data):
    return UserRegisterForm(data=user_data)

@pytest.mark.django_db
def test_user_type(signup_form):
    assert signup_form.is_valid()
    assert isinstance(signup_form.save(commit=False), User)

@pytest.mark.django_db
def test_profile_type(profile_form):
    assert profile_form.is_valid()
    assert isinstance(profile_form.save(commit=False), Profile)

@pytest.mark.django_db
def test_status_type(status_form):
    assert status_form.is_valid()
    assert isinstance(status_form.save(commit=False), Status)

@pytest.mark.django_db
def test_follower_type(form):
    assert form.is_valid()
    assert isinstance(form.save(commit=False), Follower)

@pytest.mark.django_db
def test_add_same_user(signup_form, user):
    assert not signup_form.is_valid()

@pytest.mark.django_db
def test_profile_values(profile_form, profile_data):
    note = profile_form.save(commit=False)
    assert note.city == profile_data["city"]    
