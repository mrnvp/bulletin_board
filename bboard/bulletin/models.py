from django.db import models
from django.contrib.auth.models import User

from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    CATEGORY_NAME_CHOICES = [
        ('tanks', 'Tanks'),
        ('healers', 'Healers'),
        ('dd', 'DD'),
        ('merchants', 'Merchants'),
        ('guild_masters', 'Guild Masters'),
        ('quest_givers', 'Quest Givers'),
        ('blacksmiths', 'Blacksmiths'),
        ('tanners', 'Tanners'),
        ('potion_makers', 'Potion Makers'),
        ('spellmasters', 'Spellmasters'),
    ]
    
    title = models.CharField(max_length=255)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=30, choices=CATEGORY_NAME_CHOICES, default='tanks')
    author = models.ForeignKey(User, on_delete=models.CASCADE)    
    
    def __str__(self):
        return self.title
    
class Reply(models.Model):
    content = models.TextField(max_length=1000)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_replies')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_replies')
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)   
    is_accepted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Reply from {self.sender} to {self.recipient}"
    