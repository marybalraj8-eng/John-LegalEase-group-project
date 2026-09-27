import sys
import os

# Dynamically add the project root directory to Python path to prevent ModuleNotFoundError
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import requests
from ai_core.generator import format_pdf, format_docx, sanitize_text, format_html_preview

# Configure Streamlit Web Page Layout
st.set_page_config(
    page_title="LegalEase - AI Legal Document Generator",
    page_icon="⚖️",
    layout="wide"
)

# Application Header
st.title("⚖️ LegalEase - AI Legal Document Generator")
st.caption("Generate professional, legally sound documents using Google Gemini AI.")

st.divider()

# Input Form Layout
st.subheader("📝 Enter Document Details")

col_left, col_right = st.columns(2)

with col_left:
    document_type = st.text_input(
        "Document Type", 
        placeholder="e.g., House Rent Agreement, NDA, Service Contract"
    )
    parties = st.text_input(
        "Parties Involved", 
        placeholder="e.g., R. Sundaram (Landlord), K. Karthik (Tenant)"
    )

with col_right:
    dates = st.text_input(
        "Effective Date", 
        placeholder="e.g., October 1, 2026"
    )

terms = st.text_area(
    "Specific Terms & Conditions", 
    placeholder="Enter key clauses, payment terms, deposit details, notice periods, penalties...",
    height=120
)

# Initialize Session State Variable for Generated Document
if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""

# Generate Button Action
if st.button("🚀 Generate Document", use_container_width=True):
    if not document_type or not parties:
        st.warning("Please fill in at least the Document Type and Parties Involved before generating.")
    else:
        with st.spinner("Generating legal document via AI... Please wait."):
            try:
                # Send request to FastAPI backend
                response = requests.post(
                    "http://localhost:8000/generate",
                    json={
                        "document_type": document_type,
                        "parties": parties,
                        "dates": dates,
                        "terms": terms
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    raw_text = result.get("document", "") or result.get("generated_document", "")
                    
                    # Sanitize text immediately before saving to session state
                    st.session_state.generated_text = sanitize_text(raw_text)
                    st.success("Document Generated Successfully!")
                else:
                    st.error(f"Backend API Error ({response.status_code}): {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to FastAPI Backend. Make sure Uvicorn server is running at http://localhost:8000")
            except Exception as e:
                st.error(f"Unexpected Error: {str(e)}")

# Display Editable Preview and Download Buttons
if st.session_state.generated_text:
    st.divider()
    st.subheader("✏️ Edit Document Content")
    st.info("💡You can directly edit the text in the box below and download the PDF/DOCX.")
    
    # Editable Text Area for generated content
    edited_text = st.text_area(
        "Document Text Editor",
        value=st.session_state.generated_text,
        height=350
    )
    
    # Keep session state updated with edited text
    st.session_state.generated_text = edited_text
    clean_display_text = sanitize_text(st.session_state.generated_text)
    
    st.divider()
    st.subheader("📥 Download Options")
    
    btn_col1, btn_col2 = st.columns(2)
    
    file_prefix = document_type.strip().replace(' ', '_') if document_type else 'Legal_Document'
    
    with btn_col1:
        try:
            pdf_bytes = format_pdf(clean_display_text, document_type or "Legal Document")
            st.download_button(
                label="📄 Download PDF",
                data=pdf_bytes,
                file_name=f"{file_prefix}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as pdf_err:
            st.error(f"Failed to generate PDF: {str(pdf_err)}")
        
    with btn_col2:
        try:
            docx_bytes = format_docx(clean_display_text, document_type or "Legal Document")
            st.download_button(
                label="📝 Download DOCX",
                data=docx_bytes,
                file_name=f"{file_prefix}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        except Exception as docx_err:
            st.error(f"Failed to generate DOCX: {str(docx_err)}")