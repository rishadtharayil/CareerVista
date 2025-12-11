from rest_framework import serializers
from django.contrib.auth import get_user_model
from careers.serializers import UserProgressSerializer, CareerListSerializer

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    progress = UserProgressSerializer(many=True, read_only=True)
    # saved_careers = CareerListSerializer(many=True) # Todo: Add saved_careers M2M to User if needed

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'progress']
