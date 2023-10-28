from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin  # Для ограничения доступа
from django.core.paginator import Paginator # Для добавления страниц
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy, resolve
from django.template.loader import render_to_string
from django.conf import settings
from django.core.cache import cache

from .filters import *
from .forms import *
from .models import *

DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL


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
    # queryset = Post.objects.all()

    # def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
    #     obj = cache.get(f'post-{self.kwargs["pk"]}', None)
    #     # кэш очень похож на словарь, и метод get действует также. Он забирает значение по ключу, если его нет, то забирает None.
    #
    #     # если объекта нет в кэше, то получаем его и записываем в кэш
    #     if not obj:
    #         obj = super().get_object(queryset=self.queryset)
    #         cache.set(f'post-{self.kwargs["pk"]}', obj)
    #
    #     return obj


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
        context['filter'] = Post(self.request.GET, queryset=self.get_queryset())
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

class UserView(TemplateView):
    template_name = 'pages/user_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.filter(subscribers=self.request.user)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['subscribers'] = category
        return context


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


class CategoryList(ListView):
    model = Category
    template_name = 'pages/category_list.html'
    context_object_name = 'categories'
    ordering = ['name']
    paginate_by = 10


class CategoryDetail(DetailView):
    model = Category
    template_name = 'pages/category_detail.html'
    context_object_name = 'category_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostCategoryView(ListView):
    model = Post
    template_name = 'pages/category_detail.html'
    context_object_name = 'post'  # это имя списка, в котором будут лежать все объекты,
    ordering = ['-date']  # сортировка
    paginate_by = 10  # поставим постраничный вывод в один элемент

    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        c = Category.objects.get(id=self.id)
        queryset = Post.objects.filter(category=c)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(id=self.id)
        context['is_not_subscribed'] = self.request.user not in category.subscribers.all()
        context['subscribers'] = category.subscribers.all()
        context['category'] = category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)

    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        email = user.email
        html = render_to_string(
            'pages/mail_subscribed.html',
            {
                'category': category,
                'user': user,
            },
        )
        msg = EmailMultiAlternatives(
            subject=f'Подписка на {category}',
            body='',
            from_email=DEFAULT_FROM_EMAIL,  # в settings.py
            to=[email, ],  # список получателей
        )
        msg.attach_alternative(html, 'text/html')
        try:
            msg.send()
        except Exception as e:
            print(e)
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))  # возвращает на страницу


@login_required
def unsubscribe(request, pk):  # отписка от категории
    user = request.user
    c = Category.objects.get(id=pk)

    if c.subscribers.filter(id=user.id).exists():  #проверяем есть ли у нас такой подписчик
        c.subscribers.remove(user) # то удаляем нашего пользователя
    return redirect(request.META.get('HTTP_REFERER'))



