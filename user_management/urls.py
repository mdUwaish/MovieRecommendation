from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Login, Register, verify_otp, Profile, ProfileDetail, ResetPassword, UpdatePassword

urlpatterns = [
    path('register/', Register.as_view()),
    path('login/', Login.as_view()),
    path('login/verify/', verify_otp.as_view()),
    path('profile/', Profile.as_view()),
    path('profile/detail/', ProfileDetail.as_view()),
    path('password/reset/', ResetPassword.as_view()),
    path('password/update/<token>/', UpdatePassword.as_view()),
]