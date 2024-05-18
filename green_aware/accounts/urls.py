from django.urls import path
from .views import register_user, login_user, verify_email

urlpatterns = [
    path('signup/', register_user, name='signup'),
    path('login/', login_user, name='login-user'),
    path('verify-email/<uidb64>/<token>/', verify_email, name='verify-email'),
]
