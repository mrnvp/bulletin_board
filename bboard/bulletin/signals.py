from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.core.mail import send_mail

from .models import Reply

@receiver(post_save, sender = Reply)
def send_reply(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        author_email = post.author.email
        sender_user = instance.sender
        sender_email = instance.sender.email

        send_mail(
            subject='Новый отклик на ваше объявление',
            message=f'Пользователь {sender_user.username} откликнулся на ваше объявление "{post.title}".\n\nТекст отклика:\n{instance.content}',
            from_email='mironovap0li@yandex.ru',
            recipient_list=[author_email],
        )
        
        send_mail(
            subject='Вы отправили отклик на объявление',
            message=f'Вы откликнулись на объявление "{post.title}".\n\nВаш отклик:\n{instance.content}',
            from_email='mironovap0li@yandex.ru',
            recipient_list=[sender_email],
        )

@receiver(post_save, sender=Reply)
def notify_accepted_reply(sender, instance, created, **kwargs):
    if not created and instance.is_accepted:
        send_mail(
            subject='Ваш отклик был принят',
            message=f'Ваш отклик на объявление "{instance.post.title}" был принят!',
            from_email='mironovap0li@yandex.ru',
            recipient_list=[instance.sender.email],
        )