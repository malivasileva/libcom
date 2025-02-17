from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .forms import LoginUserForm, SignupForm, UserUpdateForm


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


def settings_view(request):
    if request.method == 'POST':
        # Форма изменения имени и фамилии
        if 'first_name' in request.POST and 'last_name' in request.POST:
            user_form = UserUpdateForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Ваши данные были обновлены!')
                return redirect('users:settings')
            else:
                messages.error(request, 'Ошибка при обновлении данных.')

        # Форма изменения пароля
        elif 'password1' in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)  # Обновляем сессию
                messages.success(request, 'Пароль был успешно изменен!')
                return redirect('users:settings')
            else:
                messages.error(request, 'Ошибка при смене пароля.')

    else:
        # Для GET-запроса создаем формы
        user_form = UserUpdateForm(instance=request.user)  # Форма для имени и фамилии
        password_form = PasswordChangeForm(user=request.user)  # Форма для смены пароля

    return render(request, 'users/settings.html', {'user_form': user_form, 'password_form': password_form})




def delete_profile(request):
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        return redirect('home')  # Перенаправляем на главную страницу
