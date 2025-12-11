from django.contrib import admin
from .models import Career, Roadmap, RoadmapStep, Resource, UserProgress

class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 1

class RoadmapStepInline(admin.TabularInline):
    model = RoadmapStep
    extra = 1

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ResourceInline]
    search_fields = ('title', 'tags')

@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ('title', 'career', 'difficulty_level')
    list_filter = ('difficulty_level', 'career')
    inlines = [RoadmapStepInline]

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'career')
    list_filter = ('resource_type',)

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'roadmap_step', 'status', 'updated_at')
    list_filter = ('status',)
