# PDF Reader Utility
import pdfplumber
import warnings

warnings.filterwarnings('ignore')

def read_pdf_text(pdf_path):
    """Extract text from PDF using multiple methods for better accuracy"""
    text = ""
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Method 1: Standard text extraction
            t = page.extract_text()
            if t:
                text += t + "\n"
            
            # Method 2: Extract tables and convert to text
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    for row in table:
                        if row:
                            # Join non-None cells with spaces
                            row_text = " ".join([str(cell) if cell else "" for cell in row])
                            text += row_text + "\n"
            
            # Method 3: Try with layout preservation
            if not t or len(t) < 100:  # If standard extraction failed or got little text
                t_layout = page.extract_text(layout=True)
                if t_layout and len(t_layout) > len(t or ""):
                    text += t_layout + "\n"
    
    return text
