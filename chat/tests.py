from django.test import TestCase
from rest_framework.test import APIClient
from chat.models import ChatSession

class ChatAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_start_session(self):
        response = self.client.post('/api/chat/start/')
        self.assertEqual(response.status_code, 201)
        self.assertTrue('session_id' in response.data)
        self.session_id = response.data['session_id']

    def test_send_message(self):
        # Start session first
        start_res = self.client.post('/api/chat/start/')
        session_id = start_res.data['session_id']
        
        # Send message
        response = self.client.post(f'/api/chat/{session_id}/message/', {'message': 'Hello'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('response' in response.data)
