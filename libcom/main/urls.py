from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('search/', views.search_view, name='search'),
    #path('mybooks', views.mybooks, name='mybooks'),
    path('about', views.about, name='about')
    ]