from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.generic import ListView, DetailView
from .models import Career, Roadmap, UserProgress
from .serializers import (
    CareerListSerializer, CareerDetailSerializer, 
    RoadmapSerializer, UserProgressSerializer
)

class CareerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Career.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return CareerListSerializer
        return CareerDetailSerializer

class RoadmapViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Roadmap.objects.all()
    serializer_class = RoadmapSerializer
    permission_classes = [permissions.AllowAny]

class UserProgressViewSet(viewsets.ModelViewSet):
    serializer_class = UserProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CareerListView(ListView):
    model = Career
    template_name = 'career_list.html'
    context_object_name = 'careers'

class CareerDetailView(DetailView):
    model = Career
    template_name = 'career_detail.html'
    context_object_name = 'career'
