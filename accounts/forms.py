
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

User = get_user_model()
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username","email",)
        # field_classes = {'username': UsernameField}