from django.conf import settings
import requests
from django.shortcuts import render
from .forms import CityForm
from datetime import datetime

def get_weather(city):
    api_key = settings.API_NINJAS_API_KEY
    api_url = f'https://api.api-ninjas.com/v1/weather?city={city}'
    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    if response.status_code == 200:
        return response.json()
    else:
        return None

def weather_view(request):
    form = CityForm()
    weather_data = None

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            weather_data = get_weather(city)
            if weather_data:
                # Convert UNIX timestamps to human-readable format
                weather_data['sunrise'] = datetime.fromtimestamp(weather_data['sunrise']).strftime('%Y-%m-%d %H:%M:%S')
                weather_data['sunset'] = datetime.fromtimestamp(weather_data['sunset']).strftime('%Y-%m-%d %H:%M:%S')
    
    context = {
        'form': form,
        'weather_data': weather_data,
    }
    return render(request, 'weather/weather.html', context)

