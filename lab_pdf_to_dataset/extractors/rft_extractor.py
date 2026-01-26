# RFT (Renal Function Test) Extractor
import re
from extractors.cbc_extractor import extract_basic_info

RFT_TESTS = {
    "Urea": ["Urea"],
    "BUN": ["BUN"],
    "Creatinine": ["Creatinine"],
    "GFR": ["GFR"],
    "Uric Acid": ["Uric Acid"]
}

def extract_rft(text):
    data = extract_basic_info(text)

    # Flexible patterns to handle both PDF and Word formats
    patterns = {
        'Urea': r'Urea\s*:?\s*([0-9]+\.?[0-9]*)(?:\s*mg/dL)?',
        'BUN': r'BUN\s*:?\s*([0-9]+\.?[0-9]*)(?:\s*mg/dL)?',
        'Creatinine': r'Creatinine\s*:?\s*([0-9]+\.?[0-9]*)(?:\s*mg/dL)?',
        'GFR': r'GFR\s*:?\s*([0-9]+\.?[0-9]*)(?:\s*mL/min)?',
        'Uric Acid': r'Uric\s+Acid\s*:?\s*([0-9]+\.?[0-9]*)(?:\s*mg/dL)?'
    }
    
    for test, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data[test] = match.group(1)
        else:
            data[test] = ""

    return data
