from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
generator = GeminiDocumentGenerator()

class DocumentRequest(BaseModel):
    document_type: str = ""
    doc_type: str = ""
    parties: str = ""
    terms: str = ""
    dates: str = ""
    effective_date: str = ""

@router.post("/generate")
async def generate_doc(req: DocumentRequest):
    try:
        doc_type = req.document_type or req.doc_type or "Agreement"
        date_val = req.dates or req.effective_date or ""
        
        generated_text = generator.generate(
            document_type=doc_type,
            parties=req.parties,
            terms=req.terms,
            dates=date_val
        )
        return {"status": "success", "document": generated_text, "generated_document": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))