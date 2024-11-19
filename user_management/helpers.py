from django.contrib.auth.backends import BaseBackend
from django.core.mail import send_mail
from django.conf import settings
from .models import User

import uuid

class PhoneNumberBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        try:
            user = User.objects.get(phone_number=phone_number)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None


def send_forget_password_mail(email, token):
    subject= 'You Forget Password Token'
    message= token
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)
    return True