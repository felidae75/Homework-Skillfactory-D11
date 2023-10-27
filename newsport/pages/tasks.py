from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings


def get_subscriber(category):
    # Отдельный цикл, чтобы вытащить мэйлы
    users_email = []
    for user in category.subscribers.all():
        users_email.append(user.email)
    return users_email


def new_post_subscription(instance):
    # Письмо для подписчиков на "категорию". вызывается в signals.py
    template = 'pages/mail_new_post.html'  # шаблон

    for category in instance.category.all():
        email_subject = f'Новый пост в категории: "{category}"'
        user_emails = get_subscriber(category)

        html = render_to_string(
            template_name=template,
            context={
                'category': category,
                'post': instance,
            },
        )
        msg = EmailMultiAlternatives(
            subject=email_subject,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=user_emails
        )

        msg.attach_alternative(html, 'text/html')
        msg.send()


def week_posts_subscription(instance):
    template = 'pages/mail_weekly_posts.html'

