from .forms import LoginUserForm, SignupForm

def login_and_signup_forms(request):
    return {
        'login_form': LoginUserForm(),
        'signup_form': SignupForm()
    }