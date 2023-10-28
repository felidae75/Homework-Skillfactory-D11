# from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.urls import path
from .views import *

app_name = 'auth'
urlpatterns = [
    path('test_protect_page/', IndexViewProtect.as_view(), name='test_protect_page'),
    path('test_page/', cache_page(60)(IndexView.as_view()), name='test_page'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('signup/', UserRegisterView.as_view(), name='signup'),
    # path('user/', UserView.as_view(), name='user_page'),
    path('upgrade/', upgrade_me, name ='upgrade'),
]