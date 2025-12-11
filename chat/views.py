from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .service import ChatService
from .serializers import ChatSessionSerializer, ChatMessageSerializer
from .models import ChatSession

class ChatViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny] 
    # Use AllowAny for public chat (MVP), optional Auth later
    lookup_field = 'pk'

    @action(detail=False, methods=['post'], url_path='start')
    def start_session(self, request):
        user = request.user
        session = ChatService.start_session(user)
        serializer = ChatSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='message', lookup_field='pk')
    def process_message(self, request, pk=None):
        # pk is session_id (UUID)
        serializer = ChatMessageSerializer(data=request.data)
        if serializer.is_valid():
            try:
                result = ChatService.process_message(pk, serializer.validated_data['message'])
                return Response(result)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
