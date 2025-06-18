from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from allauth.account.views import SignupView, LoginView
from allauth.account.forms import LoginForm
from .forms import CustomSignupForm
from .models import EmailVerificationSignUp

class CustomSignupView(SignupView):
    form_class = CustomSignupForm

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect('verify_email')

class CustomLoginView(LoginView):
    form_class = LoginForm
    
    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect('post_list')
    

def verify_email(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            verification = EmailVerificationSignUp.objects.get(code=code)
            user = verification.user
            verification.is_verified = True
            verification.save()
            user.is_active = True
            user.save()
            login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
            messages.success(request, 'Код прошел успешно')
            return redirect('post_list')
        except EmailVerificationSignUp.DoesNotExist:
            messages.error(request, 'Неверный код')

    return render(request, 'accounts/verify_email.html')
               
    
    
