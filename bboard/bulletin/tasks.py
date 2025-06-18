from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.conf import settings

import datetime

from .models import Post

@shared_task
def action_every_sunday_3pm():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days = 7)
    posts = Post.objects.filter(created_at__gte = last_week)
    users = User.objects.filter(is_active = True)
    
    html_content = render_to_string(
        'email/weekly_email.html',
        {
            'posts': posts,    
        } 
    )
    
    msg = EmailMultiAlternatives(
         subject = 'Все объявления за неделю',
         body = '',
         from_email = settings.DEFAULT_FROM_EMAIL,
         to = [user.email for user in users if user.email],
    
    )
    
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    