import os
from google import genai

class GeminiDocumentGenerator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def generate_document(self, doc_type: str, details: str) -> str:
        if not self.client:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")
            
        prompt = f"""
        You are a professional legal expert. Draft a clear, formal, and legally structured {doc_type} document based on the following details:
        
        Details provided by user:
        {details}
        
        Requirements:
        - Include proper legal title, headings, clauses, and signature sections.
        - Ensure professional tone and clean formatting suitable for conversion to PDF or DOCX.
        """
        
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text