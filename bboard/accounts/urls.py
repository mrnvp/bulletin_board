from django.urls import path, include
from .views import verify_email, CustomSignupView, CustomLoginView

urlpatterns = [
    path('signup/', CustomSignupView.as_view(), name='account_signup'),
    path('login/', CustomLoginView.as_view(), name='account_login'),
    path('', include('allauth.urls')),
    path('verify-email/', verify_email, name= 'verify_email')
]
