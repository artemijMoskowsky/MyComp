

from django.urls import path
from django.contrib.auth.views import LoginView
from .views import *

urlpatterns = [
    path("registration/", RegisterView.as_view(), name="registration"),
    path("login/", LoginView.as_view(template_name = "login.html"), name="login")
]