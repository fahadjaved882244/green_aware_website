from django import forms

class UserRegistrationForm(forms.Form):
  email = forms.EmailField(label='Email')
  password = forms.CharField(label='Password', widget=forms.PasswordInput)
  name = forms.CharField(label='Name')

class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
