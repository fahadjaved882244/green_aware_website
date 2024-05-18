import requests
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegistrationForm, UserLoginForm
from django.utils.http import urlsafe_base64_decode, url_has_allowed_host_and_scheme
from django.contrib.auth.tokens import default_token_generator
from .utils import send_verification_email
from django.urls import reverse

def register_user(request):
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      name = form.cleaned_data['name']
      # Prepare the payload for the API request
      payload = {
        'email': email,
        'password': password,
        'name': name
      }
      # Send the POST request to the backend service
      response = requests.post('http://127.0.0.1:5000/users/register', json=payload)
      if response.status_code == 201:
        user = User.objects.create_user(username=email, email=email, password=password)
        user.is_active = False  # Deactivate account until it is verified
        user.save()
        send_verification_email(user, request)
        return HttpResponse('Registration successful. Please check your email to verify your account.')
      else:
        return HttpResponse(f'Failed to register user: {response.content}', status=response.status_code)
  else:
    form = UserRegistrationForm()
  return render(request, 'register.html', {'form': form})


def login_user(request):
  if request.method == 'POST':
    form = UserLoginForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      payload = {
        'email': email,
        'password': password
      }
      response = requests.post('http://127.0.0.1:5000/users/login', json=payload)
      if response.status_code == 200:
        data = response.json()
        access_token = data.get('access_token')
        refresh_token = data.get('refresh_token')
        # Store tokens in the session
        request.session['access_token'] = access_token
        request.session['refresh_token'] = refresh_token
        # Get the next parameter from the request to redirect after login
        next_url = request.GET.get('next')
        if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
          next_url = reverse('submit-observation')
        return redirect(next_url)
      else:
        return HttpResponse(f'Failed to login: {response.content}', status=response.status_code)
  else:
    form = UserLoginForm()
  return render(request, 'login.html', {'form': form})


def verify_email(request, uidb64, token):
  try:
      uid = urlsafe_base64_decode(uidb64).decode()
      user = User.objects.get(pk=uid)
  except (TypeError, ValueError, OverflowError, User.DoesNotExist):
      user = None

  if user is not None and default_token_generator.check_token(user, token):
      user.is_active = True
      user.save()
      message = "Email verification successful. You can now log in."
  else:
      message = "Email verification failed. The verification link is invalid or has expired."
  
  return render(request, 'verify_email.html', {'message': message})