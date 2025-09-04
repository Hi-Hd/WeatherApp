# dashboard/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # API endpoints for JavaScript to call
    path('api/city-search/', views.city_search_api, name='city_search_api'),
    path('api/autocomplete/', views.city_autocomplete, name='city_autocomplete'),
    path('api/weather-by-coords/', views.weather_by_coords_api, name='weather_by_coords_api'),
]