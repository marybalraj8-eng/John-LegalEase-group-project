import sys
import os
import base64
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Render-ல் ModuleNotFoundError வராமல் இருக்க Root Path-ஐக் கண்டறிந்து சேர்க்கிறது
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai_core.gemini_generator import GeminiDocumentGenerator
from utils.formatter import format_pdf, format_docx

router = APIRouter()
generator = GeminiDocumentGenerator()

class DocumentRequest(BaseModel):
    doc_type: str
    details: str

@router.post("/generate")
async def generate_legal_doc(request: DocumentRequest):
    try:
        # Generate text using Gemini
        content = generator.generate_document(request.doc_type, request.details)
        
        # Format to PDF & DOCX
        pdf_bytes = format_pdf(content, title=request.doc_type)
        docx_bytes = format_docx(content, title=request.doc_type)
        
        # Encode bytes to Base64 strings for JSON response
        pdf_b64 = base64.b64encode(pdf_bytes).decode('utf-8')
        docx_b64 = base64.b64encode(docx_bytes).decode('utf-8')
        
        return {
            "status": "success",
            "content": content,
            "pdf_b64": pdf_b64,
            "docx_b64": docx_b64
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))