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
    # Try multiple name patterns
    name = re.search(r"Patient'?s?\s*Name\s*:?\s*([A-Za-z\s]+)", text, re.IGNORECASE)
    if not name:
        name = re.search(r"Name\s*:?\s*([A-Za-z\s]+)", text, re.IGNORECASE)
    
    # Try multiple age/sex patterns
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

    # Flexible patterns to handle both PDF and Word formats
    patterns = {
        'HB': r'(?:HGB|Hemoglobin|HB)\s+([0-9]+\.?[0-9]*)\s*(?:g/dl|g\/dL)?',
        'WBC': r'WBC\s*(?:Count)?\s+([0-9]+\.?[0-9]*)\s*(?:x10|×10)?',
        'RBC': r'RBC\s*(?:Count)?\s+([0-9]+\.?[0-9]*)\s*(?:x10|×10)?',
        'Platelets': r'(?:PLATELET|Platelets?)\s*(?:COUNT)?\s+([0-9]+)\s*(?:x10|×10)?',
        'HCT': r'(?:HCT|Hematocrit)\s+([0-9]+\.?[0-9]*)\s*%?',
        'MCV': r'MCV\s+([0-9]+\.?[0-9]*)\s*(?:fL|fl)?',
        'MCH': r'MCH\s+([0-9]+\.?[0-9]*)\s*(?:pg|PG)?',
        'MCHC': r'MCHC\s+([0-9]+\.?[0-9]*)\s*(?:g/dL|g\/dl)?',
        'Neutrophils': r'Neutrophils?\s+([0-9]+)\s*%?',
        'Lymphocytes': r'Lymphocytes?\s+([0-9]+)\s*%?',
        'Monocytes': r'Monocytes?\s+([0-9]+)\s*%?',
        'Eosinophils': r'(?:Eosinophils?|Eosinophil)\s+([0-9]+)\s*%?',
        'ESR': r'ESR\s+([0-9]+\.?[0-9]*)'
    }
    
    for test, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data[test] = match.group(1)

    return data
