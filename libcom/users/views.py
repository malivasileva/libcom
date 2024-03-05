from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'main/sign-up-form.html'
    extra_context = {'title' : 'Авторизация'}
def login_user (request):
    return HttpResponse("login")

def logout_user (request):
    return HttpResponse("logout")