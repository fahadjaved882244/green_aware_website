# utils.py
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_link = request.build_absolute_uri(
        reverse('verify-email', args=[uid, token])
    )
    subject = 'Verify your email address'
    message = f'Please click the link below to verify your email address:\n\n{verification_link}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
