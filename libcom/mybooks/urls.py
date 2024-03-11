from . import views
from django.urls import path

app_name = "mybooks"

urlpatterns = [
    path('', views.index, name='index'),
    path('save_rating/<str:isbn>/', views.save_rating, name='save_rating'),
    ]