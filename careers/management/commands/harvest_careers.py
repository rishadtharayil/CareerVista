from django.core.management.base import BaseCommand
from careers.models import Career, Roadmap, RoadmapStep
from careers.ai_service import CareerGenerator
from django.utils.text import slugify
import time

class Command(BaseCommand):
    help = 'Harvests new careers using AI based on a topic'

    def add_arguments(self, parser):
        parser.add_argument('--topic', type=str, default='Technology', help='Industry or topic (e.g., Healthcare, Space)')
        parser.add_argument('--count', type=int, default=3, help='Number of careers to generate')

    def handle(self, *args, **options):
        topic = options['topic']
        count = options['count']
        
        self.stdout.write(f"Harvesting {count} careers for topic: {topic}...")
        
        generator = CareerGenerator()
        titles = generator.generate_career_titles(topic, count)
        
        if not titles:
            self.stdout.write(self.style.ERROR("Failed to generate titles."))
            return

        self.stdout.write(f"Found titles: {titles}")

        for title in titles:
            slug = slugify(title)
            if Career.objects.filter(slug=slug).exists():
                self.stdout.write(self.style.WARNING(f"Skipping existing: {title}"))
                continue

            self.stdout.write(f"Generating details for: {title}...")
            data = generator.generate_career_details(title)
            
            if not data:
                self.stdout.write(self.style.ERROR(f"Failed to get details for {title}"))
                continue

            # Save Career
            career = Career.objects.create(
                title=data.get('title', title),
                slug=slug,
                short_description=data.get('short_description', ''),
                long_description=data.get('long_description', ''),
                day_in_life=data.get('day_in_life', ''),
                skills=data.get('skills', []),
                salary_range_min=data.get('salary_range_min'),
                salary_range_max=data.get('salary_range_max'),
                demand_note=data.get('demand_note', ''),
                misconceptions=data.get('misconceptions', ''),
                tags=data.get('tags', []) + [slugify(topic)],
                seo_meta={"title": title, "generated_by": "gemini"}
            )

            # Save Roadmap
            steps_data = data.get('roadmap_steps', [])
            if steps_data:
                roadmap = Roadmap.objects.create(
                    career=career,
                    title=f"Roadmap to {title}",
                    description=f"AI generated path to becoming a {title}.",
                    difficulty_level="intermediate"
                )
                
                for step in steps_data:
                    RoadmapStep.objects.create(
                        roadmap=roadmap,
                        order=step.get('order', 1),
                        title=step.get('title', 'Step'),
                        description=step.get('description', ''),
                        estimated_time=step.get('estimated_time', ''),
                        difficulty=step.get('difficulty', '')
                    )
            
            self.stdout.write(self.style.SUCCESS(f"Saved: {title}"))
            # Rate limiting sleep just in case
            time.sleep(1)
        
        self.stdout.write(self.style.SUCCESS("Harvest complete!"))
