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

    def extract_value(test_name):
        # Find test line and next 2-3 lines (covers all formats)
        match = re.search(rf'{test_name}[^\n]*(?:\n[^\n]*?){{0,3}}', text, re.IGNORECASE | re.DOTALL)
        if not match:
            return ""
        
        section = match.group(0)
        
        # Find all standalone numbers (not part of "X - Y" or "X-Y" ranges)
        # Use negative lookbehind and lookahead to avoid range numbers
        numbers = re.findall(r'(?<![-\d])([0-9]+\.?[0-9]+)(?!\s*-\s*[0-9])', section)
        
        if not numbers:
            return ""
        
        # Return the LAST number (result appears after reference ranges)
        return numbers[-1]
    
    data['Total Bilirubin'] = extract_value(r'(?:Bilirubin\s+Total|Total\s+Bilirubin)')
    data['Direct Bilirubin'] = extract_value(r'(?:Direct\s+Bilirubin|Bilirubin\s+Conjugated)')
    data['Indirect Bilirubin'] = extract_value(r'(?:Indirect\s+Bilirubin|Bilirubin\s+Unconjugated)')
    data['ALT'] = extract_value(r'(?:SGPT|S\.G\.P\.T|ALT)')
    data['AST'] = extract_value(r'(?:SGOT|S\.G\.O\.T|AST)')
    data['ALP'] = extract_value(r'(?:Alkaline\s+Phosphatase|ALP)')
    data['Albumin'] = extract_value(r'Albumin')
    data['Total Protein'] = extract_value(r'Total\s+Protein')

    return data
