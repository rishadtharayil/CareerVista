from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Career(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=500)
    long_description = models.TextField()
    day_in_life = models.TextField(blank=True)
    skills = models.JSONField(default=list, help_text="List of required skills")
    salary_range_min = models.IntegerField(null=True, blank=True)
    salary_range_max = models.IntegerField(null=True, blank=True)
    demand_note = models.CharField(max_length=200, blank=True)
    misconceptions = models.TextField(blank=True)
    tags = models.JSONField(default=list, help_text="List of tags e.g. ['tech', 'creative']")
    seo_meta = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('course', 'Course'),
        ('article', 'Article'),
        ('video', 'Video'),
        ('book', 'Book'),
        ('tool', 'Tool'),
    ]
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=500)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    description = models.TextField(blank=True)
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='resources', null=True, blank=True)

    def __str__(self):
        return self.title

class Roadmap(models.Model):
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='roadmaps')
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.career.title} - {self.title}"

class RoadmapStep(models.Model):
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE, related_name='steps')
    order = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    estimated_time = models.CharField(max_length=100, help_text="e.g. '2 weeks'")
    resources = models.JSONField(default=list, blank=True, help_text="List of resource objects or links")
    example_project = models.TextField(blank=True)
    difficulty = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.roadmap.title} Step {self.order}: {self.title}"

class UserProgress(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    roadmap_step = models.ForeignKey(RoadmapStep, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'roadmap_step')
