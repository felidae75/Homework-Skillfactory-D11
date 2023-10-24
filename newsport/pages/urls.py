from django.urls import path
from .views import *

# app_name = 'pages'
urlpatterns = [
    path('', PostView.as_view(), name='posts_view'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('', PostsSort.as_view()),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('add/', CreatePost.as_view(), name='create_post'),
]