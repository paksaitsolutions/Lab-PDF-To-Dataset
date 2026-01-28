# CBC Extractor - Hybrid: handles same-line and next-line results
import re

def extract_basic_info(text):
    # Try multiple name patterns - stop at Sample, Registered, Age
    name = re.search(r"Patient\s*Name\s*:\s*([A-Z][A-Za-z\s\.]+?)(?:\s{2,}|\n|Age|Registration|Sample)", text, re.IGNORECASE)
    if not name:
        name = re.search(r"Name\s*:\s*([A-Z][A-Za-z\s\.]+?)(?:\s{2,}|\n|Registered|Age|F/H|Sample)", text, re.IGNORECASE)
    if not name:
        name = re.search(r"Patient['\"]?s?\s+Name\s*:?\s*([A-Z][A-Za-z\s\.]+?)(?:Sample|Registered|Age)", text, re.IGNORECASE)
    
    # Try Age/Gender patterns
    age_sex = re.search(r"Age\s*/\s*(?:Sex|Gender)\s*:\s*(\d+)\s*(?:Year|Yr).*?/\s*(Male|Female|M|F)", text, re.IGNORECASE)
    if not age_sex:
        age_sex = re.search(r"Age/Gender\s*:\s*(\d+)\s*years?\s*/\s*(Male|Female|M|F)", text, re.IGNORECASE)
    if not age_sex:
        age_sex = re.search(r"Age\s*:\s*(\d+).*?(?:Sex|Gender)\s*:\s*(Male|Female|M|F)", text, re.IGNORECASE)
    
    return {
        "Name": name.group(1).strip().rstrip('.').strip() if name else "",
        "Age": age_sex.group(1) if age_sex else "",
        "Gender": age_sex.group(2) if age_sex else ""
    }

def extract_cbc(text):
    data = extract_basic_info(text)
    
    for test in ["HB", "RBC", "HCT", "MCV", "MCH", "MCHC", "Platelets", "WBC", 
                 "Neutrophils", "Lymphocytes", "Monocytes", "Eosinophils", "ESR"]:
        data[test] = ""
    
    lines = text.split('\n')
    
    # Test definitions
    test_defs = [
        (r'hemoglobin.*\bhb\b|\bhb\b.*hemoglobin', 'HB', 5.0, 20.0, ['hba1c']),
        (r'red blood cell|\brbc\b|total rbc', 'RBC', 2.0, 7.0, []),
        (r'hematocrit|hct\b|pcv\b', 'HCT', 20.0, 60.0, ['mchc']),
        (r'mean cell volume|mcv\b', 'MCV', 50.0, 110.0, ['mchc']),
        (r'mean cell hemoglobin|\bmch\b(?!c)', 'MCH', 15.0, 40.0, []),
        (r'mean cell.*conc|mchc\b', 'MCHC', 25.0, 37.0, []),
        (r'platelet', 'Platelets', 50, 1000, []),
        (r'white blood cell|wbc\b|tlc\b', 'WBC', 2.0, 30.0, []),
        (r'neutrophil', 'Neutrophils', 10.0, 95.0, []),
        (r'lymphocyte', 'Lymphocytes', 5.0, 90.0, []),
        (r'monocyte', 'Monocytes', 1.0, 15.0, []),
        (r'eosinophil', 'Eosinophils', 0.0, 10.0, []),
        (r'\besr\b', 'ESR', 0, 100, ['test'])
    ]
    
    # Collect tests with line numbers
    tests_found = []
    for i, line in enumerate(lines):
        line_lower = line.lower()
        for pattern, test_name, min_val, max_val, exclusions in test_defs:
            if re.search(pattern, line_lower):
                if any(excl in line_lower for excl in exclusions):
                    continue
                if not any(t[0] == test_name for t in tests_found):
                    tests_found.append((test_name, min_val, max_val, i, line))
                break
    
    if not tests_found:
        return data
    
    # Try to extract values from same line first
    for test_name, min_val, max_val, line_num, line in tests_found:
        # Get rightmost numbers from test line
        numbers = re.findall(r'\b(\d+\.?\d*)\b', line)
        
        for num in reversed(numbers):
            # Skip if DIRECTLY part of a range (number-number pattern)
            if re.search(r'\d+\.?\d*\s*[-–]\s*' + re.escape(num) + r'(?!\d)', line) or \
               re.search(r'(?<!\d)' + re.escape(num) + r'\s*[-–]\s*\d+\.?\d*', line):
                continue
            
            try:
                val = float(num)
                if min_val <= val <= max_val:
                    data[test_name] = num
                    break
            except:
                pass
    
    # For tests still missing values, collect from next-line vertical column
    missing_tests = [(t, mn, mx, ln) for t, mn, mx, ln, _ in tests_found if not data[t]]
    
    if missing_tests:
        # Collect values from lines between tests (non-test lines)
        test_line_nums = {t[3] for t in tests_found}
        start_line = tests_found[0][3]
        end_line = tests_found[-1][3] + 3
        
        next_line_values = []
        for i in range(start_line, min(end_line, len(lines))):
            if i in test_line_nums:
                continue
            
            line = lines[i]
            if len(line) < 50:
                continue
            
            # Get rightmost number
            right_part = line[-40:]
            numbers = re.findall(r'\b(\d+\.?\d*)\b', right_part)
            if numbers:
                num = numbers[-1]
                if not re.search(r'\d+\.?\d*\s*[-–]\s*' + re.escape(num) + r'(?!\d)', right_part) and \
                   not re.search(r'(?<!\d)' + re.escape(num) + r'\s*[-–]\s*\d+\.?\d*', right_part):
                    next_line_values.append(num)
        
        # Map to missing tests by position
        for idx, (test_name, min_val, max_val, _) in enumerate(missing_tests):
            if idx < len(next_line_values):
                try:
                    val = float(next_line_values[idx])
                    if min_val <= val <= max_val:
                        data[test_name] = next_line_values[idx]
                except:
                    pass
    
    return data
