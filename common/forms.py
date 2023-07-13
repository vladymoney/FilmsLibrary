from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Comment


class UserRegistrationForm(UserCreationForm):
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('profile_pic', 'email', 'username', 'password1', 'password2')
class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)