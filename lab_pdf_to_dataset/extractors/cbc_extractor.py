# CBC (Complete Blood Count) Extractor
import re

CBC_TESTS = {
    "HB": ["Hemoglobin", "HB"],
    "RBC": ["RBC", "Red Blood Cell"],
    "HCT": ["Hematocrit", "HCT"],
    "MCV": ["MCV"],
    "MCH": ["MCH"],
    "MCHC": ["MCHC"],
    "Platelets": ["Platelets"],
    "WBC": ["WBC", "TLC"],
    "Neutrophils": ["Neutrophils"],
    "Lymphocytes": ["Lymphocytes"],
    "Monocytes": ["Monocytes"],
    "Eosinophils": ["Eosinophil"],
    "ESR": ["ESR"]
}

def extract_basic_info(text):
    # Try multiple name patterns - stop at newline or common keywords
    name = re.search(r"Patient'?s?\s*Name\s*:?\s*([A-Za-z\s]+?)(?:\n|Registration|Lab|Age|Sample|$)", text, re.IGNORECASE)
    if not name:
        name = re.search(r"Name\s*:?\s*([A-Za-z\s]+?)(?:\n|Registration|Lab|Age|Sample|$)", text, re.IGNORECASE)
    
    # Try multiple age/sex patterns
    age_sex = re.search(r"Age\s*/\s*Sex\s*:?\s*(\d+)\s*Years?.*?/\s*(Male|Female)", text, re.IGNORECASE)
    if not age_sex:
        age_sex = re.search(r"Age[/\s]*Sex\s*:?\s*(\d+)\s*Year.*?(Male|Female)", text, re.IGNORECASE)
    if not age_sex:
        age_sex = re.search(r"Age\s*:?\s*(\d+).*?(Male|Female)", text, re.IGNORECASE)

    return {
        "Name": name.group(1).strip() if name else "",
        "Age": age_sex.group(1) if age_sex else "",
        "Gender": age_sex.group(2) if age_sex else ""
    }

def extract_cbc(text):
    data = extract_basic_info(text)
    
    # Initialize all fields as empty
    for test in CBC_TESTS.keys():
        data[test] = ""

    # Flexible patterns - capture the LAST number on the line (the actual result)
    patterns = {
        'HB': r'(?:HGB|Hemoglobin|HB).*?g/dl[^\n]*?([0-9]+\.?[0-9]*)',
        'WBC': r'(?:White Blood Cell|WBC|TLC).*?\*10[^\n]*?([0-9]+\.?[0-9]*)',
        'RBC': r'(?:Red Blood Cell|RBC).*?\*10[^\n]*?([0-9]+\.?[0-9]*)',
        'Platelets': r'Platelets?\s*Count.*?\*10[^\n]*?([0-9]+)',
        'HCT': r'(?:HCT|PCV).*?%[^\n]*?([0-9]+\.?[0-9]*)',
        'MCV': r'(?:Mean Cell Volume|MCV).*?fl[^\n]*?([0-9]+\.?[0-9]*)',
        'MCH': r'(?:Mean Cell Hemoglobin|MCH)(?!C).*?pg[^\n]*?([0-9]+\.?[0-9]*)',
        'MCHC': r'(?:Mean Cell.*?Conc|MCHC).*?%[^\n]*?([0-9]+\.?[0-9]*)',
        'Neutrophils': r'Neutrophils?[^\n]*?%[^\n]*?([0-9]+\.?[0-9]*)',
        'Lymphocytes': r'Lymphocytes?[^\n]*?%[^\n]*?([0-9]+\.?[0-9]*)',
        'Monocytes': r'Monocytes?[^\n]*?%[^\n]*?([0-9]+\.?[0-9]*)',
        'Eosinophils': r'Eosinophils?[^\n]*?%[^\n]*?([0-9]+\.?[0-9]*)',
        'ESR': r'ESR[^\n]*?([0-9]+\.?[0-9]*)'
    }
    
    for test, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data[test] = match.group(1).strip()

    return data
