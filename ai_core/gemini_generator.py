import os
import google.generativeai as genai

class GeminiDocumentGenerator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    def generate_document(self, doc_type: str, details: str) -> str:
        if not self.model:
            raise ValueError("GEMINI_API_KEY is not set.")
            
        prompt = f"""
        You are a professional legal expert. Draft a clear, formal, and legally structured {doc_type} document based on the following details:
        
        Details provided by user:
        {details}
        
        Requirements:
        - Include proper legal title, headings, clauses, and signature sections.
        - Ensure professional tone and clean formatting suitable for conversion to PDF or DOCX.
        """
        
        response = self.model.generate_content(prompt)
        return response.text