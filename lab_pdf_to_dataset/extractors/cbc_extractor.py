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
    # Pattern 1: Name on next line after "Patient Name:" (common in multi-column layouts)
    name = re.search(r"Patient\s*Name\s*:[^\n]*\n\s*([A-Za-z\s\.]+?)(?:\s{2,}|\n)", text, re.IGNORECASE)
    
    if not name:
        # Pattern 2: Name on same line
        name = re.search(r"Patient\s*Name\s*:\s*([A-Za-z\s\.]+?)(?:\s{2,}|\n)", text, re.IGNORECASE)
    if not name:
        name = re.search(r"Patient'?s?\s*Name\s*:?\s*([A-Za-z\s\.]+?)(?:\n|Registration|Lab|Age|Sample|$)", text, re.IGNORECASE)
    if not name:
        name = re.search(r"Name\s*:?\s*([A-Za-z\s\.]+?)(?:\n|Registration|Lab|Age|Sample|$)", text, re.IGNORECASE)
    
    # Try direct Age/Sex pattern first: "Age/Sex: 18 Yr(s) / Male"
    age_sex = re.search(r"Age/Sex\s*:\s*(\d+)\s*Yr\(s\)\s*/\s*(Male|Female)", text, re.IGNORECASE)
    if not age_sex:
        age_sex = re.search(r"Age\s*/\s*Sex\s*:\s*(\d+)\s*Yr\(s\)\s*/\s*(Male|Female)", text, re.IGNORECASE)
    if not age_sex:
        age_sex = re.search(r"Age\s*/\s*Sex\s*:\s*(\d+)\s*Years?\s*/\s*(Male|Female)", text, re.IGNORECASE)
    if not age_sex:
        age_sex = re.search(r"Age[/\s]*Sex\s*:\s*(\d+)\s*Year.*?/\s*(Male|Female)", text, re.IGNORECASE)
    
    if age_sex:
        age = age_sex.group(1)
        gender = age_sex.group(2)
    else:
        # Pattern for Age/Sex on next line (multi-column layouts)
        age_sex_line = re.search(r"Age/Sex\s*:[^\n]*\n\s*([^\n]+)", text, re.IGNORECASE)
        
        if age_sex_line:
            age_match = re.search(r"(\d+)\s*Yr\(s\)\s*/\s*(Male|Female)", age_sex_line.group(1), re.IGNORECASE)
            if not age_match:
                age_match = re.search(r"(\d+)\s*Year\(s\)\s*/\s*(Male|Female)", age_sex_line.group(1), re.IGNORECASE)
            if not age_match:
                age_match = re.search(r"(\d+)\s*Yr\\?\(s\)\s*/\s*(Male|Female)", age_sex_line.group(1), re.IGNORECASE)
            if age_match:
                age = age_match.group(1)
                gender = age_match.group(2)
            else:
                age = ""
                gender = ""
        else:
            age = ""
            gender = ""

    return {
        "Name": name.group(1).strip().rstrip('.').strip() if name else "",
        "Age": age,
        "Gender": gender
    }

def extract_cbc(text):
    data = extract_basic_info(text)
    
    # Initialize all fields as empty
    for test in CBC_TESTS.keys():
        data[test] = ""

    # Try table-based extraction first (more accurate for structured PDFs)
    table_data = extract_from_table_format(text)
    if table_data:
        data.update(table_data)
        # If we got good data from table, return it
        if sum(1 for v in table_data.values() if v) >= 5:  # At least 5 fields extracted
            return data
    
    # Fallback to regex patterns
    extract_with_patterns(text, data)
    return data

def extract_from_table_format(text):
    """Extract CBC values from table-like text structure"""
    data = {}
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        line_lower = line.lower().strip()
        
        # Look for test names and extract the last number on the line (the result)
        # Pattern: Test_Name ... Reference_Range ... Unit ... Result_Value
        
        if 'hemoglobin' in line_lower and 'hb' in line_lower:
            if 'hba1c' not in line_lower and 'hbsag' not in line_lower:
                match = re.search(r'[↓↑]?\s*(\d+\.\d+)\s*$', line)
                if match:
                    data['HB'] = match.group(1)
        
        elif line_lower.startswith('hb') and 'hba1c' not in line_lower:
            match = re.search(r'(\d+\.?\d*)\s*$', line)
            if match:
                data['HB'] = match.group(1)
        
        elif 'red blood cell' in line_lower and 'rbc' in line_lower:
            match = re.search(r'(\d+\.\d+)\s*$', line)
            if match:
                data['RBC'] = match.group(1)
        
        elif line_lower.startswith('rbc') or line_lower.startswith('total rbc'):
            match = re.search(r'(\d+\.\d+)\s*$', line)
            if match:
                data['RBC'] = match.group(1)
        
        elif 'tlc' in line_lower and not data.get('WBC'):
            match = re.search(r'(\d+\.\d+)\s*$', line)
            if match:
                data['WBC'] = match.group(1)
        
        elif 'hematocrit' in line_lower and 'hct' in line_lower:
            match = re.search(r'[↓↑]?\s*(\d+\.\d+)\s*$', line)
            if match:
                data['HCT'] = match.group(1)
        
        elif line_lower.startswith('hct') or line_lower.startswith('hematocrit'):
            match = re.search(r'[↓↑]?\s*(\d+\.?\d*)\s*$', line)
            if match:
                data['HCT'] = match.group(1)
        
        elif 'mean cell volume' in line_lower and 'mcv' in line_lower:
            match = re.search(r'(\d+\.\d+)\s*$', line)
            if match:
                data['MCV'] = match.group(1)
        
        elif line_lower.startswith('mcv') and 'mchc' not in line_lower:
            match = re.search(r'(\d+\.?\d*)\s*$', line)
            if match:
                data['MCV'] = match.group(1)
        
        elif 'mean cell hemoglobin' in line_lower and 'mch' in line_lower and 'mchc' not in line_lower:
            match = re.search(r'(\d+\.\d+)\s*$', line)
            if match:
                data['MCH'] = match.group(1)
        
        elif line_lower.startswith('mch') and 'mchc' not in line_lower:
            match = re.search(r'(\d+\.?\d*)\s*$', line)
            if match:
                data['MCH'] = match.group(1)
        
        elif 'mean cell hb conc' in line_lower or ('mchc' in line_lower and 'mean' in line_lower):
            match = re.search(r'(\d+\.\d+)\s*$', line)
            if match:
                data['MCHC'] = match.group(1)
        
        elif line_lower.startswith('mchc'):
            match = re.search(r'(\d+\.?\d*)\s*$', line)
            if match:
                data['MCHC'] = match.group(1)
        
        elif 'platelets count' in line_lower or 'platelet count' in line_lower:
            match = re.search(r'(\d+)\s*$', line)
            if match:
                data['Platelets'] = match.group(1)
        
        elif 'white blood cell' in line_lower and ('wbc' in line_lower or 'tlc' in line_lower):
            match = re.search(r'(\d+\.\d+)\s*$', line)
            if match:
                data['WBC'] = match.group(1)
        
        elif line_lower.startswith('wbc') and not data.get('WBC'):
            match = re.search(r'(\d+\.?\d*)\s*$', line)
            if match:
                data['WBC'] = match.group(1)
        
        elif 'neutrophil' in line_lower:
            match = re.search(r'(\d+\.?\d*)\s*$', line)
            if match:
                data['Neutrophils'] = match.group(1)
        
        elif 'lymphocyte' in line_lower:
            match = re.search(r'(\d+\.?\d*)\s*$', line)
            if match:
                data['Lymphocytes'] = match.group(1)
        
        elif 'monocyte' in line_lower:
            match = re.search(r'(\d+\.?\d*)\s*$', line)
            if match:
                data['Monocytes'] = match.group(1)
        
        elif 'eosinophil' in line_lower:
            match = re.search(r'(\d+\.?\d*)\s*$', line)
            if match:
                data['Eosinophils'] = match.group(1)
        
        elif 'esr' in line_lower:
            match = re.search(r'(\d+\.?\d*)\s*$', line)
            if match:
                data['ESR'] = match.group(1)
    
    return data

def extract_with_patterns(text, data):
    """Extract using regex patterns as fallback"""
    # Flexible patterns - capture the result value after the unit
    # Pattern strategy: Look for test name, then unit, then capture the LAST number on that section
    patterns = {
        'HB': [
            r'(?:HGB|Hemoglobin|Hb)\s+[\d\s\-\.]+\s+g/dl\s+([0-9]+\.?[0-9]*)',
            r'(?:HGB|Hemoglobin|Hb)[^\n]*?g/dl[\s\n]+([0-9]+\.?[0-9]*)'
        ],
        'WBC': [
            r'(?:WBC|TLC|White Blood Cell)\s*(?:Count)?\s+[\d\s\-\.]+\s+[x\*]10\^?\d+[/\s]*[lL]\s+([0-9]+\.?[0-9]*)',
            r'(?:WBC|TLC|White Blood Cell)[^\n]*?[x\*]10\^?\d+[/\s]*[lL][\s\n]+([0-9]+\.?[0-9]*)'
        ],
        'RBC': [
            r'(?:Total\s+)?(?:RBC|Red Blood Cell)\s+[\d\s\-\.]+\s+[x\*]10\^?\d+[/\s]*[lL]\s+([0-9]+\.?[0-9]*)',
            r'(?:Total\s+)?(?:RBC|Red Blood Cell)[^\n]*?[x\*]10\^?\d+[/\s]*[lL][\s\n]+([0-9]+\.?[0-9]*)'
        ],
        'Platelets': [
            r'Platelets?\s*Count\s+[\d\s\-\.]+\s+[x\*]10\^?\d+[/\s]*[lL]\s+([0-9]+)',
            r'Platelets?\s*Count[^\n]*?[x\*]10\^?\d+[/\s]*[lL][\s\n]+([0-9]+)'
        ],
        'HCT': [
            r'(?:HCT|PCV|Hematocrit)\s+[\d\s\-\.]+\s+%\s+([0-9]+\.?[0-9]*)',
            r'(?:HCT|PCV|Hematocrit)[^\n]*?%[\s\n]+([0-9]+\.?[0-9]*)'
        ],
        'MCV': [
            r'MCV\s+[\d\s\-\.]+\s+fl\s+([0-9]+\.?[0-9]*)',
            r'(?:Mean Cell Volume|MCV)[^\n]*?fl[\s\n]+([0-9]+\.?[0-9]*)'
        ],
        'MCH': [
            r'MCH(?!C)\s+[\d\s\-\.]+\s+pg\s+([0-9]+\.?[0-9]*)',
            r'(?:Mean Cell Hemoglobin|MCH)(?!C)[^\n]*?pg[\s\n]+([0-9]+\.?[0-9]*)'
        ],
        'MCHC': [
            r'MCHC\s+[\d\s\-\.]+\s+(?:g/dl|%)\s+([0-9]+\.?[0-9]*)',
            r'(?:Mean Cell.*?Conc|MCHC)[^\n]*?(?:g/dl|%)[\s\n]+([0-9]+\.?[0-9]*)'
        ],
        'Neutrophils': [
            r'Neutrophils?\s+[\d\s\-\.]+\s+%\s+([0-9]+\.?[0-9]*)',
            r'Neutrophils?[^\n]*?%[\s\n]+([0-9]+\.?[0-9]*)'
        ],
        'Lymphocytes': [
            r'Lymphocytes?\s+[\d\s\-\.]+\s+%\s+([0-9]+\.?[0-9]*)',
            r'Lymphocytes?[^\n]*?%[\s\n]+([0-9]+\.?[0-9]*)'
        ],
        'Monocytes': [
            r'Monocytes?\s+[\d\s\-\.]+\s+%\s+([0-9]+\.?[0-9]*)',
            r'Monocytes?[^\n]*?%[\s\n]+([0-9]+\.?[0-9]*)'
        ],
        'Eosinophils': [
            r'Eosinophils?\s+[\d\s\-\.]+\s+%\s+([0-9]+\.?[0-9]*)',
            r'Eosinophils?[^\n]*?%[\s\n]+([0-9]+\.?[0-9]*)'
        ],
        'ESR': [
            r'ESR[^\n]*?([0-9]+\.?[0-9]*)'
        ]
    }
    
    for test, pattern_list in patterns.items():
        # Skip if already extracted by table method
        if data.get(test):
            continue
            
        # Try each pattern until one matches
        if isinstance(pattern_list, str):
            pattern_list = [pattern_list]
        
        for pattern in pattern_list:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                data[test] = match.group(1).strip()
                break
