# PDF Reader Utility
import pdfplumber
import warnings
import sys
import os
import shutil

try:
    from pdf2image import convert_from_path
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("⚠️ OCR dependencies not found. Install pdf2image and pytesseract for scanned PDFs.")

warnings.filterwarnings('ignore')

def check_ocr_dependencies():
    """Check if Tesseract and Poppler are installed and accessible."""
    if not OCR_AVAILABLE:
        return ["pdf2image or pytesseract Python packages"]
    
    missing = []
    
    # Check Tesseract
    if not shutil.which('tesseract'):
        # Check common Windows paths
        common_tesseract_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            os.path.expanduser(r"~\AppData\Local\Tesseract-OCR\tesseract.exe")
        ]
        found_tesseract = False
        for path in common_tesseract_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                found_tesseract = True
                break
        
        if not found_tesseract:
            missing.append("Tesseract-OCR")

    # Check Poppler (pdftoppm or pdftocairo)
    if not (shutil.which('pdftoppm') or shutil.which('pdftocairo')):
        # Check common Windows paths for Poppler is harder as it's often manual extract
        # We can try to guess if it's in PATH or a known location, but usually it needs PATH.
        missing.append("Poppler (pdftoppm/pdftocairo)")
    
    return missing

def read_pdf_text(pdf_path):
    """
    Extract text from PDF using layout-preserving method.
    Falls back to OCR if text extraction yields minimal results (scanned PDF).
    """
    text = ""
    
    try:
        # First attempt: standard text extraction
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Use layout-preserving extraction for better unit-based pattern matching
                page_text = page.extract_text(layout=True)
                if page_text:
                    text += page_text + "\n"
        
        # Check if extracted text is sufficient (heuristic: > 50 chars)
        # If not, it might be a scanned PDF
        if len(text.strip()) < 50:
            missing_deps = check_ocr_dependencies()
            if not missing_deps:
                print(f"ℹ️ Low text count ({len(text.strip())} chars). Attempting OCR for {os.path.basename(pdf_path)}...")
                try:
                    images = convert_from_path(pdf_path)
                    ocr_text = ""
                    for i, image in enumerate(images):
                        page_ocr_txt = pytesseract.image_to_string(image)
                        ocr_text += page_ocr_txt + "\n"
                    
                    if len(ocr_text.strip()) > len(text.strip()):
                        text = ocr_text
                        print("✅ OCR successful")
                    else:
                        print("⚠️ OCR yielded less text than standard extraction.")
                except Exception as e:
                    print(f"❌ OCR failed: {e}")
                    # Keep original text (even if empty/small) if OCR fails
            else:
                print(f"⚠️ OCR Required but dependencies missing for {os.path.basename(pdf_path)}")
                print(f"❌ Missing: {', '.join(missing_deps)}")
                print("👉 Please install Tesseract-OCR and Poppler and add them to your PATH.")
                
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""
    
    return text
