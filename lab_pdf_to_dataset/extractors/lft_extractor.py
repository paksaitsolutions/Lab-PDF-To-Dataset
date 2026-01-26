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

    # More specific patterns to get result value (not normal range)
    patterns = {
        'Total Bilirubin': r'Total\s+Bilirubin\s+([0-9]+\.?[0-9]*)\s*(?:mg/dL|\s)',
        'Direct Bilirubin': r'Direct\s+Bilirubin\s+([0-9]+\.?[0-9]*)\s*(?:mg/dL|\s)',
        'Indirect Bilirubin': r'Indirect\s+Bilirubin\s+([0-9]+\.?[0-9]*)\s*(?:mg/dL|\s)',
        'ALT': r'(?:ALT|SGPT)\s+([0-9]+\.?[0-9]*)\s*(?:U/L|\s)',
        'AST': r'(?:AST|SGOT)\s+([0-9]+\.?[0-9]*)\s*(?:U/L|\s)',
        'ALP': r'(?:ALP|Alkaline\s+Phosphatase)\s+([0-9]+\.?[0-9]*)\s*(?:U/L|\s)',
        'Albumin': r'Albumin\s+([0-9]+\.?[0-9]*)\s*(?:g/dL|\s)',
        'Total Protein': r'Total\s+Protein\s+([0-9]+\.?[0-9]*)\s*(?:g/dL|\s)'
    }
    
    for test, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data[test] = match.group(1)
        else:
            data[test] = ""

    return data
