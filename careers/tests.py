from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from careers.models import Career, Roadmap

class CareerModelTests(TestCase):
    def test_create_career(self):
        career = Career.objects.create(title="Test Career", slug="test-career")
        self.assertEqual(str(career), "Test Career")

class CareerAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.career = Career.objects.create(title="API Career", slug="api-career", short_description="Desc")

    def test_get_careers(self):
        response = self.client.get('/api/careers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_career_detail(self):
        response = self.client.get(f'/api/careers/{self.career.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], "API Career")
