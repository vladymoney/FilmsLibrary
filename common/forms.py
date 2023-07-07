from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('profile_pic', 'email', 'username', 'password1', 'password2')
