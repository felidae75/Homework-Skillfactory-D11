from django.contrib.auth import authenticate
from django.shortcuts import render
from django.views.generic import TemplateView
# from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import *
from .forms import *


# Тестовые страницы, чтобы проверять работоспособность
class IndexViewProtect(LoginRequiredMixin, TemplateView):
    template_name = 'pages/test_protect_page.html'


class IndexView(TemplateView):
    template_name = 'pages/test_page.html'


class UserView(TemplateView):
    template_name = 'pages/user_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'pages/register.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        # group = Group.objects.get(name='my_group')
        group = Group.objects.get_or_create(name='users')[0]

        user.groups.add(group)  # добавляем нового пользователя в эту группу
        user.save()
        return super().form_valid(form)


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


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')
