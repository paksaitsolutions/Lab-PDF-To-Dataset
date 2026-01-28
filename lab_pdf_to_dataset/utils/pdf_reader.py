# PDF Reader Utility
import pdfplumber
import warnings

warnings.filterwarnings('ignore')

def read_pdf_text(pdf_path):
    """Extract text from PDF using layout-preserving method"""
    text = ""
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Use layout-preserving extraction for better unit-based pattern matching
            page_text = page.extract_text(layout=True)
            if page_text:
                text += page_text + "\n"
    
    return text
