from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.urls import path
from .views import *

app_name = 'pages'
urlpatterns = [
    path('', PostView.as_view(), name='posts_view'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('', PostsSort.as_view()),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('user/', UserView.as_view(), name='user_page'),
    path('add/', CreatePostView.as_view(), name='create_post'),
    path('<int:pk>/edit', PostUpdate.as_view(), name='update_post'),
    path('<int:pk>/delete', PostDelete.as_view(), name='del_post'),
    path('сategory/', CategoryList.as_view(), name='categories'),
    path('сategory/<int:pk>', PostCategoryView.as_view(), name='category_detail'),
    path('<int:pk>/subscribe/', subscribe, name='subscribe'),
    path('unsubscribe/<int:pk>', unsubscribe, name='unsubscribe'),
]