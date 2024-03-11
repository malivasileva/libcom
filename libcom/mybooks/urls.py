from . import views
from django.urls import path

app_name = "mybooks"

urlpatterns = [
    path('', views.index, name='index'),
    path('statistic.html', views.statistic, name='statistic'),
    path('save_rating/<str:isbn>/', views.save_rating, name='save_rating'),
    path('save_read/<str:isbn>/', views.save_read, name='save_read'),
    path('save_want/<str:isbn>/', views.save_want, name='save_want'),
    ]