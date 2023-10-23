from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *


class PostView(ListView):
    model = Post
    template_name = 'pages/news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-date')


class PostDetail(DetailView):
    model = Post
    template_name = 'pages/post.html'
    context_object_name = 'post'
