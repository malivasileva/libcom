from . import views
from django.urls import path

app_name = "search"

urlpatterns = [
    path('results/<str:query>/', views.search_results_view, name='search_results'),
    ]