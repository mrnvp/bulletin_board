from allauth.account.forms import SignupForm
import random
from .models import EmailVerificationSignUp
from django.core.mail import send_mail

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        
    
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.is_active = False 
        user.save()
        
        code = str(random.randint(100000, 999999))
        
        EmailVerificationSignUp.objects.update_or_create(user = user, 
        defaults={  
        'code': code,
        'is_verified': False
        })
        
        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтверждения: {code}',
            from_email='mironovap0li@yandex.ru',
            recipient_list=[user.email],
        )
        
        return user