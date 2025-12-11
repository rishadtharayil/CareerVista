from rest_framework import serializers
from .models import ChatSession

class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ['session_id', 'created_at', 'updated_at']

class ChatMessageSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)
