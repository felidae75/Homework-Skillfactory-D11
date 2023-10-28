from django import template
from datetime import datetime

register = template.Library()

@register.filter
def lower(value):
    # Фильтр делает буквы меньше
    return value.lower()


@register.simple_tag
def current_time(format_string):
    # Вернет текущее время в формате, который передается в качестве аргумента тэга.
    return datetime.now().strftime(format_string)


@register.simple_tag(takes_context=True)
def func(context, other_arg):
    # Функция может использовать контекст шаблона. Для этого необходимо добавить аргументы у декоратора и самой функции
    pass


@register.simple_tag(takes_context=True, name="tagname")
def func(context, other_arg):
    # Название тэга, используемое в самом шаблоне, может отличаться от названия функции
    # Для указания иного имени, нужно добавить соответствующий аргумент в декоратор
    pass


