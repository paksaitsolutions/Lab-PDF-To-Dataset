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

    # Patterns to capture the LAST number on each line (actual result, not normal range)
    patterns = {
        'Urea': r'Urea[^\n]*?mg/dL[^\n]*?([0-9]+\.?[0-9]*)',
        'BUN': r'BUN[^\n]*?mg/dL[^\n]*?([0-9]+\.?[0-9]*)',
        'Creatinine': r'Creatinine[^\n]*?mg/dL[^\n]*?([0-9]+\.?[0-9]*)',
        'GFR': r'GFR[^\n]*?mL/min[^\n]*?([0-9]+\.?[0-9]*)',
        'Uric Acid': r'Uric\s+Acid[^\n]*?mg/dL[^\n]*?([0-9]+\.?[0-9]*)'
    }
    
    for test, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data[test] = match.group(1)
        else:
            data[test] = ""

    return data
