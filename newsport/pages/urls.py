from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *

app_name = 'pages'
urlpatterns = [
    path('', PostView.as_view(), name='posts_view'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('', PostsSort.as_view()),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('add/', CreatePostView.as_view(), name='create_post'),
    path('<int:pk>/edit', PostUpdate.as_view(), name='update_post'),
    path('<int:pk>/delete', PostDelete.as_view(), name='del_post'),
]