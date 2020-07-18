from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_mesages', on_delete=models.CASCADE)
    content = models.TextField()
    room_name = models.CharField(max_length=10,default = "1_2")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.author.username
    
    @staticmethod
    def last_30_messages(room_name):
        return Message.objects.filter(room_name = room_name).order_by('-timestamp')[:30]
    
class MessageUserStatus(models.Model):
    message_receiver = models.ForeignKey(User, related_name='user_mesages', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='received_message', on_delete=models.CASCADE)
    is_read = models.BooleanField(default = False)
    
    class Meta:
        unique_together = [('message_receiver','message')]