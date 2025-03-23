import os
import time
import google.generativeai as genai
from django.conf import settings

class GeminiService:
    """Service for interacting with the Gemini LLM API"""
    
    def __init__(self):
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError("Gemini API key is not set")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_summary(self, text, length='medium'):
        """
        Generate a summary of the provided text using Gemini API
        
        Args:
            text (str): The text to summarize
            length (str): Summary length - 'short', 'medium', or 'long'
            
        Returns:
            tuple: (summary, processing_time)
        """
        start_time = time.time()
        
        # Define length parameters
        length_config = {
            'short': 'a very concise 1-2 paragraph',
            'medium': 'a comprehensive 3-4 paragraph', 
            'long': 'a detailed 5-7 paragraph'
        }
        
        length_desc = length_config.get(length, length_config['medium'])
        
        try:
            # Prepare the prompt for Gemini
            prompt = f"""
            Please provide {length_desc} summary of the following document. 
            Focus on the main points, key findings, and important details.
            
            Document content:
            {text[:25000]}  # Limit text to avoid token limits
            """
            
            # Generate response
            response = self.model.generate_content(prompt)
            summary = response.text
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            return summary, processing_time
        
        except Exception as e:
            end_time = time.time()
            processing_time = end_time - start_time
            raise Exception(f"Error generating summary with Gemini API: {str(e)}")
