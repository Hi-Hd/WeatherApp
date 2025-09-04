# dashboard/views.py

from django.shortcuts import render
import requests
from django.conf import settings
from django.http import JsonResponse
import json
from pathlib import Path
from datetime import datetime

# Helper function to process weather data to avoid repeating code
def process_weather_data(city_name, api_key):
    # API call for current weather to get details and coordinates
    current_weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    current_weather_response = requests.get(current_weather_url)
    
    if current_weather_response.status_code != 200:
        return None, None, "City not found."

    cw_data = current_weather_response.json()

    # API call for 5-day forecast
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}&units=metric"
    forecast_response = requests.get(forecast_url)
    
    # Process current weather data
    weather_data = {
        'city': cw_data['name'],
        'temperature': round(cw_data['main']['temp']),
        'description': cw_data['weather'][0]['description'].title(),
        'icon': cw_data['weather'][0]['icon'],
        'feels_like': round(cw_data['main']['feels_like']),
        'humidity': cw_data['main']['humidity'],
        'wind_speed': cw_data['wind']['speed'],
        'sunrise': datetime.fromtimestamp(cw_data['sys']['sunrise']).strftime('%I:%M %p'),
        'sunset': datetime.fromtimestamp(cw_data['sys']['sunset']).strftime('%I:%M %p'),
    }

    # Process forecast data
    forecast_data = []
    if forecast_response.status_code == 200:
        fc_data = forecast_response.json()
        for forecast in fc_data['list']:
            if '12:00:00' in forecast['dt_txt']:
                forecast_data.append({
                    'date': datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S').strftime('%a'), # Short day name
                    'temp_max': round(forecast['main']['temp_max']),
                    'temp_min': round(forecast['main']['temp_min']),
                    'icon': forecast['weather'][0]['icon'],
                })
    
    return weather_data, forecast_data, None


def index(request):
    # The initial page load is now handled by JavaScript/geolocation.
    # This view will still render the base template.
    return render(request, 'dashboard/index.html')


def city_search_api(request):
    city = request.GET.get('city')
    if not city:
        return JsonResponse({'error': 'City not provided.'}, status=400)
    
    api_key = settings.OPENWEATHER_API_KEY
    weather_data, forecast_data, error = process_weather_data(city, api_key)

    if error:
        return JsonResponse({'error': error}, status=404)

    return JsonResponse({
        'weather_data': weather_data,
        'forecast_data': forecast_data
    })


def city_autocomplete(request):
    query = request.GET.get('q', '').lower()
    results = []
    if query:
        cities_file = Path(__file__).resolve().parent / "static" / "cities.json"
        with open(cities_file, "r", encoding="utf-8") as f:
            cities = json.load(f)
        results = [city for city in cities if city.lower().startswith(query)][:10]
    return JsonResponse(results, safe=False)


# NEW: View to get weather by coordinates
def weather_by_coords_api(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    if not lat or not lon:
        return JsonResponse({'error': 'Coordinates not provided.'}, status=400)

    api_key = settings.OPENWEATHER_API_KEY
    # Use reverse geocoding to get city name from coordinates
    reverse_geo_url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={api_key}"
    response = requests.get(reverse_geo_url)
    if response.status_code != 200 or not response.json():
        return JsonResponse({'error': 'Could not determine city from coordinates.'}, status=404)

    city_name = response.json()[0]['name']
    weather_data, forecast_data, error = process_weather_data(city_name, api_key)

    if error:
        return JsonResponse({'error': error}, status=404)
        
    return JsonResponse({
        'weather_data': weather_data,
        'forecast_data': forecast_data
    })