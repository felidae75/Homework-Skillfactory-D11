from django.urls import path
from .views import *

urlpatterns = [
    path('', PostView.as_view()),
    path('<int:pk>', PostDetail.as_view()),
]