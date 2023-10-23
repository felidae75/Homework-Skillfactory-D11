from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.views import View

from .models import *


class PostView(ListView):
    model = Post
    template_name = 'pages/news.html'
    context_object_name = 'news'
    ordering = ['-date']
    paginate_by = 1


class PostDetail(DetailView):
    model = Post
    template_name = 'pages/post.html'
    context_object_name = 'post'


class PostsSort(View):
    def get(self, request):
        posts = Post.objects.order_by('-date')
        p_paginator = Paginator(posts, 1)
        posts = p_paginator.get_page(request.GET.get('page', 1))

        data = {
            'posts': posts,
        }

        return render(request, 'pages/news.html', data)
