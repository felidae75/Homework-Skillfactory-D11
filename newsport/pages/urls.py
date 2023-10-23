from django.urls import path
from .views import *

app_name = 'pages'
urlpatterns = [
    path('', PostView.as_view()),
    path('<int:pk>/', PostDetail.as_view()),
    path('news/', PostsSort.as_view()),
]