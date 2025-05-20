from django.db import models
from django.contrib.auth import get_user_model

class Image(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='images')
    original = models.ImageField(upload_to='originals/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image {self.id} by {self.owner.username}"