from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm

class SignUpView(generic.CreateView):
  form_class = SignUpForm
  success_url = reverse_lazy('login')  # Redirect to login page after signup
  template_name = 'signup.html'


from django.contrib.auth.views import LoginView
from .forms import LoginForm

class CustomLoginView(LoginView):
  authentication_form = LoginForm
  template_name = 'login.html'
  redirect_authenticated_user = True  # Redirect users who are already logged in
