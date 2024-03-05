from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import LoginUserForm, SignupForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title' : 'Авторизация'}

    # def get_success_url(self):
    #     return reverse_lazy('home')

class CreateUser (CreateView):
    form_class = SignupForm
    template_name = 'users/signup.html'
    extra_context = {
         'title': 'Регистрация'
    }
    success_url = reverse_lazy('home')
    #def form_invalid(self, form):
