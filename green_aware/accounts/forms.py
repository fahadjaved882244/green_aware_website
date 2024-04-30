from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class SignUpForm(UserCreationForm):
  is_qualified = forms.BooleanField(required=True, widget=forms.CheckboxInput)

  class Meta:
    model = get_user_model()  # Returns the correct user model configured for use
    fields = ('email', 'password1', 'password2', 'is_qualified')


from django.contrib.auth.forms import AuthenticationForm
from django import forms

class LoginForm(AuthenticationForm):
  username = forms.CharField(label='Email / Username')
