from django.contrib import admin
from .models import ChatSession

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'user', 'created_at')
    readonly_fields = ('session_id', 'created_at', 'updated_at')
