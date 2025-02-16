from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignupForm

from .forms import LoginUserForm, SignupForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title' : 'Авторизация'}

    # def get_success_url(self):
    #     return reverse_lazy('home')

class CreateUser(CreateView):
    form_class = SignupForm
    template_name = 'users/signup.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # Перенаправление на главную страницу, если пользователь уже авторизован
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Регистрация прошла успешно! Пожалуйста, войдите.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка регистрации. Проверьте данные.")
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

