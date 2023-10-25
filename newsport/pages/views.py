from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin  # Для ограничения доступа
from django.core.paginator import Paginator # Для добавления страниц
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy

from .filters import *
from .forms import *
from .models import *


# Список новостей
class PostView(ListView):
    model = Post
    template_name = 'pages/news.html'
    context_object_name = 'news'
    ordering = ['-date']
    paginate_by = 10

    # Метод добавления новости. Не используется, так как пошёл на отдельную страницу
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['filter'] = MiniPostFilter(self.request.GET, queryset=self.get_queryset())
        context['choices'] = Post.TYPE_LIST
        context['form'] = CreatePostForm()
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context

    # def post(self, request, *args, **kwargs):
    # author = request.POST['author']
    # title = request.POST['title']
    # type = request.POST['type']
    # text = request.POST['text']
    # post = Post(title=title, type=type, text=text)  # создаём новый пост и сохраняем
    # post.save()
    # return super().get(request, *args, **kwargs)  # отправляем пользователя обратно на GET-запрос

    def post(self, request, *args, **kwargs):
        form = CreatePostForm(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса
        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый пост
            form.save()
        return super().get(request, *args, **kwargs)


# Страница отдельной новости
class PostDetail(DetailView):
    model = Post
    template_name = 'pages/post.html'
    context_object_name = 'post'


# Сортировщик новостей
class PostsSort(View):
    def get(self, request):
        posts = Post.objects.order_by('-date')
        p_paginator = Paginator(posts, 1)
        posts = p_paginator.get_page(request.GET.get('page', 1))

        data = {
            'posts': posts,
        }

        return render(request, 'pages/news.html', data)


# Поиск новостей
class PostSearch(ListView):
    model = Post
    template_name = 'pages/search.html'
    context_object_name = 'search'
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())

        return context


# class CreatePost(ListView):
#     model = Post
#     template_name = 'pages/add_news.html'
#     context_object_name = 'add_news'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['choices'] = Post.TYPE_LIST
#         context['form'] = CreatePostForm
#         return context
#
#     # def post(self, request, *args, **kwargs):
#     # author = request.POST['author']
#     # title = request.POST['title']
#     # type = request.POST['type']
#     # text = request.POST['text']
#     # post = Post(title=title, type=type, text=text)  # создаём новый пост и сохраняем
#     # post.save()
#     # return super().get(request, *args, **kwargs)  # отправляем пользователя обратно на GET-запрос
#
#     def post(self, request, *args, **kwargs):
#         form = CreatePostForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return super().get(request, *args, **kwargs)


# class MiniPostSearch(ListView):
#     model = Post
#     template_name = 'pages/news.html'
#     context_object_name = 'mini_search'
#     ordering = ['-date']
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['filter'] = MiniPostFilter(self.request.GET, queryset=self.get_queryset())
#
#         return context/


# Создать пост
class CreatePostView(PermissionRequiredMixin, CreateView):
    template_name = 'pages/add_news.html'
    form_class = CreatePostForm
    permission_required = ('pages.add_post',)


# Отредактировать пост
class PostUpdate(PermissionRequiredMixin, UpdateView):
    template_name = 'pages/add_news.html'
    form_class = CreatePostForm
    permission_required = ('pages.update_post',)

    def get_object(self, **kwargs):
        id_post = self.kwargs.get('pk')
        return Post.objects.get(pk=id_post)


# Удалить пост
class PostDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'pages/del_news.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('pages:posts_view')
    permission_required = ('pages.del_post',)
