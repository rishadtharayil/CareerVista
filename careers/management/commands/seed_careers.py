from django.core.management.base import BaseCommand
from careers.models import Career, Roadmap, RoadmapStep, Resource
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seeds the database with sample careers'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        careers_data = [
            ("Software Engineer", "Builds software applications.", "Coding features, debugging, meetings.", ["Python", "JavaScript", "SQL"], 70000, 150000, "High demand"),
            ("Data Scientist", "Analyzes data to find insights.", "Data cleaning, modeling, reporting.", ["Python", "Pandas", "Math"], 80000, 160000, "Growing"),
            ("Product Manager", "Oversees product development.", "Roadmapping, stakeholder meetings.", ["Communication", "Agile", "Strategy"], 90000, 180000, "Stable"),
            ("UX Designer", "Designs user experiences.", "Wireframing, user testing.", ["Figma", "Empathy", "Prototyping"], 65000, 130000, "High"),
            ("DevOps Engineer", "Manages infrastructure.", "CI/CD, cloud management.", ["Docker", "AWS", "Linux"], 90000, 170000, "Very High"),
            ("Nurse", "Provides patient care.", "Rounds, charts, patient interaction.", ["Empathy", "Medical Knowledge"], 60000, 100000, "High"),
            ("Digital Marketer", "Promotes products online.", "Ad campaigns, SEO, content.", ["SEO", "Analytics", "Writing"], 50000, 100000, "Moderate"),
            ("Cybersecurity Analyst", "Protects systems from threats.", "Monitoring, incident response.", ["Network Security", "Linux", "Forensics"], 75000, 140000, "High"),
            ("Cloud Architect", "Designs cloud infrastructure.", "Architecture planning, migration.", ["AWS", "Azure", "Security"], 120000, 200000, "High"),
            ("AI Engineer", "Builds AI models and systems.", "Training models, deployment.", ["PyTorch", "TensorFlow", "Math"], 100000, 200000, "Exploding"),
            ("Technical Writer", "Writes technical documentation.", "Writing, editing, research.", ["Writing", "Markdown", "Tech basics"], 60000, 110000, "Stable"),
            ("QA Engineer", "Tests software for bugs.", "Writing tests, manual testing.", ["Automation", "Selenium", "Detail-oriented"], 60000, 120000, "Stable"),
            ("Frontend Developer", "Builds user interfaces.", "Coding UI, integrating APIs.", ["React", "CSS", "HTML"], 70000, 140000, "High"),
            ("Backend Developer", "Builds server-side logic.", "API design, database optimization.", ["Python", "Java", "SQL"], 75000, 150000, "High"),
            ("Mobile App Developer", "Builds mobile apps.", "Coding iOS/Android apps.", ["Swift", "Kotlin", "React Native"], 80000, 150000, "High"),
            ("Game Developer", "Creates video games.", "Physics, graphics programming.", ["C++", "Unity", "Math"], 60000, 130000, "Competitive"),
            ("Blockchain Developer", "Builds decentralized apps.", "Smart contracts, cryptography.", ["Solidity", "Rust", "Crypto"], 90000, 180000, "Niche"),
            ("Sales Engineer", "Sells technical products.", "Demos, technical consultation.", ["Sales", "Tech knowledge"], 80000, 180000, "High"),
            ("HR Manager", "Manages human resources.", "Hiring, policy, conflict res.", ["Communication", "Law", "Empathy"], 60000, 120000, "Stable"),
            ("Financial Analyst", "Analyzes financial data.", "Modeling, reporting, forecasting.", ["Excel", "Accounting", "Math"], 65000, 130000, "Stable"),
        ]

        created_count = 0
        for title, short, day, skills, min_sal, max_sal, demand in careers_data:
            slug = slugify(title)
            if Career.objects.filter(slug=slug).exists():
                continue
            
            career = Career.objects.create(
                title=title,
                slug=slug,
                short_description=short,
                long_description=f"Detailed description for {title}.",
                day_in_life=day,
                skills=skills,
                salary_range_min=min_sal,
                salary_range_max=max_sal,
                demand_note=demand,
                tags=[title.lower(), "tech" if "Engineer" in title or "Developer" in title else "general"],
                seo_meta={"title": title, "description": short}
            )
            created_count += 1
            
            # Create Roadmap
            roadmap = Roadmap.objects.create(
                career=career,
                title=f"Become a {title}",
                description="Standard path.",
                difficulty_level="intermediate"
            )
            
            # Steps
            for i in range(1, 4):
                RoadmapStep.objects.create(
                    roadmap=roadmap,
                    order=i,
                    title=f"Step {i}: Basics",
                    description="Learn the fundamentals.",
                    estimated_time="1 month",
                    resources=["https://example.com/course"],
                    difficulty="beginner"
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} careers.'))
