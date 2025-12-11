from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserProfileSerializer

class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
