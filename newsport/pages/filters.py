from django_filters import FilterSet
from .models import *


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {'author': ['exact'], 'date': ['gt'], 'type': ['exact'], 'title': ['icontains'], 'rating': ['gt']}


class MiniPostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {'title': ['icontains'], 'type': ['exact']}