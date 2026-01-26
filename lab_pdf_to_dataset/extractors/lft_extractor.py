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

    # Patterns to capture the LAST number on each line (actual result, not normal range)
    patterns = {
        'Total Bilirubin': r'Total\s+Bilirubin[^\n]*?mg/dL[^\n]*?([0-9]+\.?[0-9]*)',
        'Direct Bilirubin': r'Direct\s+Bilirubin[^\n]*?mg/dL[^\n]*?([0-9]+\.?[0-9]*)',
        'Indirect Bilirubin': r'Indirect\s+Bilirubin[^\n]*?mg/dL[^\n]*?([0-9]+\.?[0-9]*)',
        'ALT': r'(?:ALT|SGPT|S\.G\.P\.T\.).*?U/L[^\n]*?([0-9]+\.?[0-9]*)',
        'AST': r'(?:AST|SGOT|S\.G\.O\.T).*?U/L[^\n]*?([0-9]+\.?[0-9]*)',
        'ALP': r'(?:ALP|Alkaline\s+Phosphatase).*?U/L[^\n]*?([0-9]+\.?[0-9]*)',
        'Albumin': r'Albumin[^\n]*?g/dL[^\n]*?([0-9]+\.?[0-9]*)',
        'Total Protein': r'Total\s+Protein[^\n]*?g/dL[^\n]*?([0-9]+\.?[0-9]*)'
    }
    
    for test, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data[test] = match.group(1)
        else:
            data[test] = ""

    return data
