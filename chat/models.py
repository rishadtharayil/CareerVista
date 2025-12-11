from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class ChatSession(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='chat_sessions')
    messages = models.JSONField(default=list, help_text="List of message objects {'role': 'user/assistant', 'content': '...'}")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session {self.session_id} ({self.user})"
