from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CareerViewSet, RoadmapViewSet, UserProgressViewSet

router = DefaultRouter()
router.register(r'careers', CareerViewSet)
router.register(r'roadmaps', RoadmapViewSet)
router.register(r'progress', UserProgressViewSet, basename='user-progress')

urlpatterns = [
    path('', include(router.urls)),
]
