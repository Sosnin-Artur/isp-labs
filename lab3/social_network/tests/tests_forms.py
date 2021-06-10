import pytest

from account.models import Profile
from account.forms import ProfileForm

from posts.models import Post
from posts.forms import PostForm

from registration.forms import UserRegisterForm

from django.contrib.auth.models import User


@pytest.fixture
def user_data():
	return {"username": "Vasya", 
           	"first_name": "vasya", "last_name": "pupkin",
   		"email": "vasya@mgmail.com",
                "password": "12345678", 
                "password2": "12345678", 
        }

@pytest.fixture
def user():
    return User.objects.create_user("Vasya", "vasya@gmail.com")

@pytest.fixture
def profile_data():
    return {"avatar": "", "gender": "M", "city": "Minsk"}

@pytest.fixture
def post_data():
    return {"post_title": "Test_Title", "post_text": "test_text"}

@pytest.fixture
def profile():
    return Profile.objects.create(data=profile_data)

@pytest.mark.django_db
def test_fail_user_reg(user_data):
    assert not UserRegisterForm(data=user_data).is_valid()

@pytest.mark.django_db
def test_post_form(post_data):
    assert PostForm(data=post_data).is_valid()

@pytest.mark.django_db
def test_fail_profile_create(profile_data):
    assert not ProfileForm().is_valid()

