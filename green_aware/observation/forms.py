# forms.py
from django import forms
from django.utils import timezone

class ObservationForm(forms.Form):
    date_time = forms.DateTimeField(label='Date and Time', initial=timezone.now)
    what3words = forms.CharField(label='What3Words')
    land_surface_temperature = forms.FloatField(label='Land Surface Temperature')
    sea_surface_temperature = forms.FloatField(label='Sea Surface Temperature')
    humidity = forms.FloatField(label='Humidity')
    wind_speed = forms.FloatField(label='Wind Speed')
    wind_direction = forms.IntegerField(label='Wind Direction')
    precipitation = forms.FloatField(label='Precipitation')
    haze = forms.FloatField(label='Haze')
    notes = forms.CharField(label='Notes', widget=forms.Textarea, required=False)
