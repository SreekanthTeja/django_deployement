from django.shortcuts import render, reverse
from .forms import *
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as Login
# Create your views here.
class SignupView(generic.CreateView):
    template_name = "accounts/registration/signup.html"
    form_class = SignUpForm

    def get_success_url(self):
        return reverse("login")

class LoginView(Login):
    template_name = "accounts/registration/login.html"
    