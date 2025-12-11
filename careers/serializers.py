from rest_framework import serializers
from .models import Career, Roadmap, RoadmapStep, Resource, UserProgress

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class RoadmapStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadmapStep
        fields = '__all__'

class RoadmapSerializer(serializers.ModelSerializer):
    steps = RoadmapStepSerializer(many=True, read_only=True)
    class Meta:
        model = Roadmap
        fields = '__all__'

class CareerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = ['id', 'title', 'slug', 'short_description', 'tags', 'difficulty_level_summary']
    
    difficulty_level_summary = serializers.SerializerMethodField()
    
    def get_difficulty_level_summary(self, obj):
        # Example logic, or separate field
        return "Varied"

class CareerDetailSerializer(serializers.ModelSerializer):
    resources = ResourceSerializer(many=True, read_only=True)
    roadmaps = RoadmapSerializer(many=True, read_only=True)
    class Meta:
        model = Career
        fields = '__all__'

class UserProgressSerializer(serializers.ModelSerializer):
    roadmap_step_title = serializers.ReadOnlyField(source='roadmap_step.title')
    roadmap_title = serializers.ReadOnlyField(source='roadmap_step.roadmap.title')
    career_title = serializers.ReadOnlyField(source='roadmap_step.roadmap.career.title')

    class Meta:
        model = UserProgress
        fields = '__all__'
        read_only_fields = ['user']
