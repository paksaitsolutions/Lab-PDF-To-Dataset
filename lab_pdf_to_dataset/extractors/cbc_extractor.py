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
    name = re.search(r"Patient Name:\s*([A-Z\s]+)", text)
    age_sex = re.search(r"Age\s*/\s*Sex:\s*(\d+).*?(Male|Female)", text)

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

    # More specific patterns to get result value (not normal range)
    patterns = {
        'HB': r'(?:HGB|Hemoglobin|HB)\s+([0-9]+\.?[0-9]*)\s*(?:g/dl|\s)',
        'WBC': r'WBC\s+(?:Count)?\s*([0-9]+\.?[0-9]*)',
        'RBC': r'RBC\s+(?:Count)?\s*([0-9]+\.?[0-9]*)',
        'Platelets': r'(?:PLATELET|Platelets)\s+(?:COUNT)?\s*([0-9]+)',
        'HCT': r'(?:HCT|Hematocrit)\s+([0-9]+\.?[0-9]*)\s*%?',
        'MCV': r'MCV\s+([0-9]+\.?[0-9]*)\s*(?:fL|\s)',
        'MCH': r'MCH\s+([0-9]+\.?[0-9]*)\s*(?:pg|\s)',
        'MCHC': r'MCHC\s+([0-9]+\.?[0-9]*)\s*(?:g/dL|\s)',
        'Neutrophils': r'Neutrophils\s+([0-9]+)',
        'Lymphocytes': r'Lymphocytes\s+([0-9]+)',
        'Monocytes': r'Monocytes\s+([0-9]+)',
        'Eosinophils': r'(?:Eosinophils|Eosinophil)\s+([0-9]+)',
        'ESR': r'ESR\s+([0-9]+)'
    }
    
    for test, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data[test] = match.group(1)

    return data
