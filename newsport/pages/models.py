from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models import Sum
# Последнее - чтобы суммировало рейтинг


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.IntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.all().aggregate(rating=Sum('rating'))
        postSumRating = 0
        postSumRating += postRat.get('rating')
        # Апдейт с рейтинга статей

        # commRat = self.authorUser.comment_set.all().aggregate(rating=Sum('rating'))
        # commentSumRating = 0
        # commentSumRating += commRat.get('rating')
        # Тут только комментарии автора вытаскивались, не подошло...

        commentsRating = Comment.objects.filter(commentPost__author=Author.objects.first()).aggregate(rating=Sum('rating'))
        commentsRatingSum = 0
        commentsRatingSum += commentsRating.get('rating')
        # Все комментарии к постам автора

        self.authorRating = postSumRating * 3 + commentsRatingSum
        self.save()
        # Надеюсь, оно правильно считает...

    def __str__(self):
        return self.authorUser.username


class Category(models.Model):
    # Категория статьи
    name = models.CharField(max_length=32, unique=True, default='no_category')
    subscribers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f'{self.name}'


# Новость или статья
class Post(models.Model):
    # Статья
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    BLOG = 'BL'
    TYPE_LIST = (
        (NEWS, "Новости"),
        (BLOG, "Статьи")
    )

    type = models.CharField(max_length=2, choices=TYPE_LIST, default=BLOG)
    date = models.DateTimeField(auto_now_add=True)
    dateChange = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128, default='Без заголовка')
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f"{self.text[0:124]} ..."

    def get_category_name(self):
        return f'{self.category.all()}'

    def get_author_name(self):
        return self.author.authorUser.username

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с постом
        return f'/news/{self.id}'

    def __str__(self):
        return f"({self.type}, {self.date}, {self.category.all()}, {self.author}, {self.title}, {self. text})"


class PostCategory(models.Model):
    # Связь многие со многими
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.categoryThrough}'


class Comment(models.Model):
    # Модель комментария
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    dateChange = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        # Костыль для вывода информации о посте
        return f'Юзверь: {self.commentUser.username}, Текст: {self.text}. Опубликован: {self.date}, Рейтинг: {self.rating}'




