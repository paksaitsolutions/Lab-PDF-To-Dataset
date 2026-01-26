# LFT (Liver Function Test) Extractor
import re
from extractors.cbc_extractor import extract_basic_info

LFT_TESTS = {
    "Total Bilirubin": ["Total Bilirubin"],
    "Direct Bilirubin": ["Direct Bilirubin"],
    "Indirect Bilirubin": ["Indirect Bilirubin"],
    "ALT": ["ALT", "SGPT"],
    "AST": ["AST", "SGOT"],
    "ALP": ["Alkaline Phosphatase"],
    "Albumin": ["Albumin"],
    "Total Protein": ["Total Protein"]
}

def extract_lft(text):
    data = extract_basic_info(text)

    # Flexible patterns to handle both PDF and Word formats
    patterns = {
        'Total Bilirubin': r'Total\s+Bilirubin\s*:?\s*([0-9]+\.?[0-9]*)(?:\s*mg/dL)?',
        'Direct Bilirubin': r'Direct\s+Bilirubin\s*:?\s*([0-9]+\.?[0-9]*)(?:\s*mg/dL)?',
        'Indirect Bilirubin': r'Indirect\s+Bilirubin\s*:?\s*([0-9]+\.?[0-9]*)(?:\s*mg/dL)?',
        'ALT': r'(?:ALT|SGPT)\s*:?\s*([0-9]+\.?[0-9]*)(?:\s*U/L)?',
        'AST': r'(?:AST|SGOT)\s*:?\s*([0-9]+\.?[0-9]*)(?:\s*U/L)?',
        'ALP': r'(?:ALP|Alkaline\s+Phosphatase)\s*:?\s*([0-9]+\.?[0-9]*)(?:\s*U/L)?',
        'Albumin': r'Albumin\s*:?\s*([0-9]+\.?[0-9]*)(?:\s*g/dL)?',
        'Total Protein': r'Total\s+Protein\s*:?\s*([0-9]+\.?[0-9]*)(?:\s*g/dL)?'
    }
    
    for test, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data[test] = match.group(1)
        else:
            data[test] = ""

    return data
