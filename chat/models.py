from django.db import models

class ChatMessage(models.Model):
    room_name = models.CharField(max_length=255, default='default_room')
    sender_name = models.CharField(max_length=255, default='Unknown')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"[{self.room_name}] {self.sender_name}: {self.message[:20]}"
