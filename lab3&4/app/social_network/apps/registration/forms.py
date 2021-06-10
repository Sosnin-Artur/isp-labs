from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.http import HttpResponse


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='login', required=True)
    first_name = forms.CharField(label='first name', required=True)
    last_name = forms.CharField(label='second name', required=True)
    email = forms.EmailField(required=True)

    error_messages = {
        'duplicate_username': "login is busy",
        'password_mismatch': "passwords mismatch",
    }

    field_order = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['email'].help_text = 'enter e-mail'
        self.fields['username'].help_text = 'can contain only letters, numbers and @ . + - _'
        self.fields['password1'].help_text = """
        password cannot be similar with username.

        password must at least 8 characters long.

        password must not be user frequently and popular.
        
        password must not consist entirely of numbers.
        """
        self.fields['password2'].help_text = 'please, repeat password.'
        self.fields['username'].widget.attrs['maxlength'] = 20
        # self.fields['username'].widget.attrs['class'] = 'w-100'
