from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailVerificationSignUp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default= False)
