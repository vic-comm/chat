from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
# User = get_user_model()
class Rooms(models.Model):
    name=models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

class Message(models.Model):
    room = models.ForeignKey(Rooms, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name='user', on_delete=models.CASCADE)
    content = models.TextField()
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)