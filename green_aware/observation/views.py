# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ObservationForm
from django.utils import timezone
import requests
import what3words

WHAT3WORDS_API_KEY = '7C3OZ2D9'

def get_coordinates(what3words_address):
    url = f'https://api.what3words.com/v3/convert-to-coordinates?words={what3words_address}&key={WHAT3WORDS_API_KEY}'
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        data = response.json()
        return data['coordinates']['lat'], data['coordinates']['lng']
    return None, None


def submit_observation(request):
    if request.method == 'POST':
        form = ObservationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            latitude, longitude = get_coordinates(data['what3words'])
            if latitude is None or longitude is None:
                return HttpResponse('Invalid What3words address', status=400)
            payload = [{
                "date_time": data['date_time'].isoformat(),
                "time_zone_offset": 1,
                "latitude": latitude,
                "longitude": longitude,
                "land_surface_temperature": data['land_surface_temperature'],
                "sea_surface_temperature": data['sea_surface_temperature'],
                "humidity": data['humidity'],
                "wind_speed": data['wind_speed'],
                "wind_direction": data['wind_direction'],
                "precipitation": data['precipitation'],
                "haze": data['haze'],
                "notes": data['notes'],
            }]
            access_token = request.session.get('access_token')
            headers = {
                'Authorization': f'Bearer {access_token}'
            }
            print(payload)
            response = requests.post('http://127.0.0.1:5000/observations/', json=payload, headers=headers)
            if response.status_code == 201:
                message = 'Observation submitted successfully'
                return render(request, 'successful.html', {'message': message})
            else:
                return HttpResponse(f'Failed to submit observation: {response.content}', status=response.status_code)
    else:
        form = ObservationForm(initial={'date_time': timezone.now()})
    return render(request, 'submit_observation.html', {'form': form})

