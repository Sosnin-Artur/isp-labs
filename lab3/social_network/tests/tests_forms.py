import pytest

from account.models import Profile
from account.forms import ProfileForm

from posts.models import Post
from posts.forms import PostForm

from registration.forms import UserRegisterForm

from django.contrib.auth.models import User


@pytest.fixture
def user_data():
    return {
        "username": "vasya",
        "email": "vasya@gmail.com",
        "password": "vasyapassword",
        "password2": "vasyapassword",
    }

@pytest.fixture
def user():
    return User.objects.create_user("Vasya", "vasya@gmail.com")

@pytest.fixture
def profile_data():
    return {"gender": "M", "user": user(), "city": "Minsk"}

@pytest.fixture
def post_data():
    return {"post_title": "Test_Title", "post_text": "test_text"}

@pytest.fixture
def profile():
    return Profile.objects.create(data=profile_data)

@pytest.mark.django_db
def test_user_reg(user_data):
    assert UserRegistrationForm(data=user_data).is_valid()

@pytest.mark.django_db
def test_post_form(post_data):
    assert PostForm(data=post_data).is_valid()

@pytest.mark.django_db
def test_profile_create(post_data):
    assert ProfileForm(data=profile_data).is_valid()

