import os
import json
from django.conf import settings
from .models import ChatSession
# import google.generativeai as genai

# genai.configure(api_key=settings.GEMINI_API_KEY)

class ChatService:
    @staticmethod
    def start_session(user=None):
        user_obj = user if user and user.is_authenticated else None
        return ChatSession.objects.create(user=user_obj)

    @staticmethod
    def process_message(session_id, message_text):
        try:
            session = ChatSession.objects.get(session_id=session_id)
        except ChatSession.DoesNotExist:
            raise ValueError("Invalid session ID")

        # History Management
        if not session.messages:
            session.messages = []
        
        session.messages.append({'role': 'user', 'content': message_text})
        
        # Gemini Integration
        api_key = os.environ.get('GEMINI_API_KEY')
        if api_key and api_key != 'todo-insert-key':
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                # Use flash model for speed and availability
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Construct history for Gemini
                # Note: Gemini history format might differ, keeping it simple mainly for logic demo
                # Simple prompt construction
                prompt = f"System: You are a helpful career coach. Answer concisely.\nUser: {message_text}"
                
                response = model.generate_content(prompt)
                response_text = response.text
            except Exception as e:
                response_text = f"Gemini Error: {str(e)}"
        else:
            # Mock Response
            response_text = f"This is a mock response to '{message_text}'. Configure GEMINI_API_KEY to get real AI responses."

        session.messages.append({'role': 'assistant', 'content': response_text})
        session.save()
        
        return {
            "session_id": str(session.session_id),
            "response": response_text,
            "suggested_careers": [] 
        }
