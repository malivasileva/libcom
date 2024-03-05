from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
        labels = {
            'Username': 'Логин',
            'Password': 'Пароль'
        }

class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Логин',
            'password1': 'Пароль',
            'password2': 'Повторите пароль'
        }