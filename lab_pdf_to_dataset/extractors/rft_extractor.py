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

    # More specific patterns to get result value (not normal range)
    patterns = {
        'Urea': r'Urea\s+([0-9]+\.?[0-9]*)\s*(?:mg/dL|\s)',
        'BUN': r'BUN\s+([0-9]+\.?[0-9]*)\s*(?:mg/dL|\s)',
        'Creatinine': r'Creatinine\s+([0-9]+\.?[0-9]*)\s*(?:mg/dL|\s)',
        'GFR': r'GFR\s+([0-9]+\.?[0-9]*)\s*(?:mL/min|\s)',
        'Uric Acid': r'Uric\s+Acid\s+([0-9]+\.?[0-9]*)\s*(?:mg/dL|\s)'
    }
    
    for test, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data[test] = match.group(1)
        else:
            data[test] = ""

    return data
