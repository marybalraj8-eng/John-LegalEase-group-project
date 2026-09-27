import io
import re
from fpdf import FPDF
from docx import Document



def sanitize_text(text: str) -> str:
    """Strictly cleans Unicode characters and markdown symbols before sending to FPDF."""
    if not text:
        return ""
    
    # Explicit replacement for common non-latin1 legal/markdown characters
    replacements = {
        '•': '-',
        '●': '-',
        '○': '-',
        '▪': '-',
        '–': '-',
        '—': '-',
        '“': '"',
        '”': '"',
        '‘': "'",
        '’': "'",
        '…': '...',
        '\u2022': '-',
        '\u2023': '-',
        '\u25e6': '-',
        '\u2043': '-',
        '\u2219': '-',
        '\u2013': '-',
        '\u2014': '-',
        '\u201c': '"',
        '\u201d': '"',
        '\u2018': "'",
        '\u2019': "'",
        '\u00a0': ' ',
    }
    
    for char, repl in replacements.items():
        text = text.replace(char, repl)
    
    # Ignore any residual unicode characters that cannot be encoded in latin-1
    return text.encode('latin-1', 'ignore').decode('latin-1')


def format_html_preview(text: str) -> str:
    """Formats markdown text into basic clean HTML for Streamlit preview."""
    if not text:
        return ""
    
    formatted = re.sub(r'^### (.*$)', r'<h3>\1</h3>', text, flags=re.M)
    formatted = re.sub(r'^## (.*$)', r'<h2>\1</h2>', formatted, flags=re.M)
    formatted = re.sub(r'^# (.*$)', r'<h1>\1</h1>', formatted, flags=re.M)
    formatted = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted)
    formatted = formatted.replace('\n', '<br>')
    return formatted


def format_docx(text: str, title: str = "Legal Document") -> bytes:
    """Generates a downloadable .docx file bytes."""
    doc = Document()
    clean_title = sanitize_text(title)
    doc.add_heading(clean_title, level=0)
    
    clean_text = sanitize_text(text)
    for paragraph in clean_text.split('\n'):
        line = paragraph.strip()
        if line:
            doc.add_paragraph(line)
            
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()


def format_pdf(text: str, title: str = "Legal Document") -> bytes:
    """Generates a downloadable .pdf file bytes safely with FPDF."""
    pdf = FPDF()
    pdf.set_margins(15, 15, 15)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    safe_text = sanitize_text(text)
    safe_title = sanitize_text(title)
    
    effective_width = pdf.epw
    
    # Document Title
    pdf.set_font("Helvetica", style="B", size=15)
    pdf.multi_cell(effective_width, 10, safe_title, align="C")
    pdf.ln(5)
    
    # Document Body
    pdf.set_font("Helvetica", size=10)
    
    for line in safe_text.split('\n'):
        line_str = line.strip()
        if not line_str:
            pdf.ln(3)
            continue
            
        pdf.set_x(15)
        clean_line = re.sub(r'\*\*(.*?)\*\*', r'\1', line_str)
        clean_line = sanitize_text(clean_line)
        
        if clean_line.startswith('#'):
            pdf.set_font("Helvetica", style="B", size=11)
            heading_text = clean_line.lstrip('#').strip()
            pdf.multi_cell(effective_width, 6, heading_text)
            pdf.set_font("Helvetica", size=10)
        elif clean_line.startswith('-') or clean_line.startswith('*'):
            bullet_content = clean_line.lstrip('-*').strip()
            pdf.multi_cell(effective_width, 5, f"  - {bullet_content}")
        else:
            pdf.multi_cell(effective_width, 5, clean_line)
            
    return bytes(pdf.output())