import os
import json
import logging
import google.generativeai as genai
from django.conf import settings

logger = logging.getLogger(__name__)

class CareerHarvesterSpec:
    """
    Defines the expected JSON structure for the AI to return.
    """
    CAREER_SCHEMA = {
        "title": "Job Title",
        "short_description": "One sentence summary.",
        "long_description": "Detailed description.",
        "day_in_life": "What a typical day looks like.",
        "skills": ["Skill 1", "Skill 2"],
        "salary_range_min": 50000,
        "salary_range_max": 100000,
        "demand_note": "High/Stable/Low",
        "misconceptions": "Common myths.",
        "tags": ["tag1", "tag2"],
        "roadmap_steps": [
            {
                "order": 1,
                "title": "Step Title",
                "description": "Step description",
                "estimated_time": "1 month",
                "difficulty": "beginner"
            }
        ]
    }

class CareerGenerator:
    def __init__(self):
        api_key = os.environ.get('GEMINI_API_KEY')
        self.has_key = api_key and api_key != 'todo-insert-key'
        if self.has_key:
            genai.configure(api_key=api_key)
            try:
                self.model = genai.GenerativeModel('gemini-2.5-flash')
            except Exception:
                # Fallback or strict error handling
                self.model = genai.GenerativeModel('gemini-pro')

    def generate_career_titles(self, topic, count=5):
        if not self.has_key:
            return [f"Mock AI {topic} Career {i}" for i in range(1, count + 1)]

        prompt = f"""
        List {count} distinct, real-world job titles related to '{topic}'.
        Return ONLY a JSON array of strings. Example: ["Career A", "Career B"]
        """
        try:
            response = self.model.generate_content(prompt)
            # Clean md code blocks if present
            text = self._clean_json_text(response.text)
            return json.loads(text)
        except Exception as e:
            logger.error(f"Error generating titles: {e}")
            return []

    def generate_career_details(self, title):
        if not self.has_key:
            return self._get_mock_career_data(title)

        prompt = f"""
        Generate detailed career information for: "{title}".
        Return a valid JSON object matching this exact structure:
        {json.dumps(CareerHarvesterSpec.CAREER_SCHEMA)}
        
        Ensure salary is integer (USD). Keep descriptions helpful and realistic.
        RETURN ONLY JSON.
        """
        try:
            response = self.model.generate_content(prompt)
            text = self._clean_json_text(response.text)
            data = json.loads(text)
            return data
        except Exception as e:
            logger.error(f"Error generating details for {title}: {e}")
            return None

    def _clean_json_text(self, text):
        # Remove potential markdown formatting ```json ... ```
        text = text.strip()
        if text.startswith("```"):
            lines = text.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines)
        return text

    def _get_mock_career_data(self, title):
        return {
            "title": title,
            "short_description": f"AI generated description for {title} (Mock).",
            "long_description": "This is a placeholder description because a valid Gemini API key was not found.",
            "day_in_life": "Debugging code, attending meetings, drinking coffee.",
            "skills": ["Mock Skill A", "Mock Skill B"],
            "salary_range_min": 60000,
            "salary_range_max": 120000,
            "demand_note": "Simulated High",
            "misconceptions": "None.",
            "tags": ["mock", "ai"],
            "roadmap_steps": [
                {
                    "order": 1,
                    "title": "Learn Basics",
                    "description": "Start with the fundamentals.",
                    "estimated_time": "2 weeks",
                    "difficulty": "beginner"
                }
            ]
        }
