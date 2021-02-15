from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    # adds email form to default user creation form
    email = forms.EmailField(required=True)
    # nested name space for configuration
    # user model will be affected, these fields will be in the form
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        # displays the users current information in profile
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        # displays the users current information in profile
        model = Profile
        fields = ['image']