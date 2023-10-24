from django.forms import ModelForm
from django import forms
from .models import *


# Создаём модельную форму
class CreatePostForm(ModelForm):
    # В класс мета, как обычно, надо написать модель, по которой будет строиться форма, и нужные нам поля. Мы уже делали что-то похожее с фильтрами
   class Meta:
       model = Post
       fields = ['author', 'title', 'text', 'type']

       widgets = {
           'author': forms.Select(attrs={
               'class': 'form-control'
           }),
           'type': forms.Select(attrs={
               'class': 'form-control'
           }),
           'category': forms.SelectMultiple(attrs={
               'class': 'form-control'
           }),
           'title': forms.TextInput(attrs={
               'class': 'form-control'
           }),
           'text': forms.Textarea(attrs={
               'class': 'form-control'
           }),
       }