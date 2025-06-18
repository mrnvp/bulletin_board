from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.shortcuts import redirect

@receiver(user_signed_up)
def after_signup(sender, request, user, **kwargs):
    return redirect('verify_email')