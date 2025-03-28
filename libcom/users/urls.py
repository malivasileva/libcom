from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('signup/', views.CreateUser.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('settings/',  views.settings_view, name='settings')
#path('settings/',  views.settings_view, name='settings')
    ]