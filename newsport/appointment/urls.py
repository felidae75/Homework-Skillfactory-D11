from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *

app_name = 'appointment'

urlpatterns = [
    path('', AppointmentView.as_view(), name="appointment"),
]
