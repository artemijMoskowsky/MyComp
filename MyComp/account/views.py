from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model

# Create your views here.
class RegisterView(CreateView):
    form_class = UserCreationForm
    model = get_user_model()
    success_url = "login"
    template_name = "registr.html"