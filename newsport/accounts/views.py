from django.contrib.auth import authenticate
from django.shortcuts import render
from django.views.generic import TemplateView
# from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *


# Тестовые страницы, чтобы проверять работоспособность
class IndexViewProtect(LoginRequiredMixin, TemplateView):
    template_name = 'pages/test_protect_page.html'


class IndexView(TemplateView):
    template_name = 'pages/test_page.html'


# class LoginNewsView(LoginView):
#     template_name = 'pages/login.html'


# class LogoutNewsView(LogoutView):
#     template_name = 'pages/logout.html'


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'pages/register.html'
    success_url = '/'


class UserLoginView(FormView):
    model = User
    form_class = UserLoginForm
    template_name = 'pages/login.html'
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class UserLogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
