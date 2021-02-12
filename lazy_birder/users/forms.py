from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    # adds email form to default user creation form
    email = forms.EmailField(required=True)
    # nested name space for configuration
    # user model will be affected, these fields will be in the form
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']