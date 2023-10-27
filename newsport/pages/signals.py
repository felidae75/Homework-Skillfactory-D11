from django.db.models.signals import post_save, m2m_changed

from django.dispatch import receiver
from .models import *
from .tasks import new_post_subscription


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, **kwargs):
    # Реагирует на новую запись "категорий" в БД
    if kwargs['action'] == 'post_add':
        new_post_subscription(instance)