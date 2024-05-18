from django.urls import path
from .views import submit_observation

urlpatterns = [
    path('submit-observation/', submit_observation, name='submit-observation'),
]
