from django.contrib import admin
from .models import *

def nullfy_raiting_post(modeladmin, request, queryset):
    # request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(rating=0)
    nullfy_raiting_post.short_description = 'Обнулить рейтинг поста'
    # описание для более понятного представления в админ панели задаётся, как будто это объект


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('authorUser', 'authorRating')
    list_filter = ('authorUser', 'authorRating')
    search_fields = ('authorUser', 'authorRating')


# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name')


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'type', 'date', 'title')
    list_filter = ('author', 'type', 'date')
    search_fields = ('author', 'date', 'title', 'text')
    actions = [nullfy_raiting_post]


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('postThrough', 'categoryThrough')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment)
