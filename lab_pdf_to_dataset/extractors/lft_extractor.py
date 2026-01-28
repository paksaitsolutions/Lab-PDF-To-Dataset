# LFT Extractor - Hybrid approach
import re
from extractors.cbc_extractor import extract_basic_info

def extract_lft(text):
    data = extract_basic_info(text)
    
    for test in ["Total Bilirubin", "Direct Bilirubin", "Indirect Bilirubin", 
                 "ALT", "AST", "ALP", "Albumin", "Total Protein"]:
        data[test] = ""
    
    lines = text.split('\n')
    
    # Test definitions with validation ranges
    test_defs = [
        (r'total\s+bilirubin|bilirubin\s+total', 'Total Bilirubin', 0.1, 30.0, []),
        (r'direct\s+bilirubin|bilirubin\s+direct|conjugated', 'Direct Bilirubin', 0.0, 15.0, []),
        (r'indirect\s+bilirubin|bilirubin\s+indirect|unconjugated', 'Indirect Bilirubin', 0.0, 20.0, []),
        (r'\balt\b|sgpt|alanine', 'ALT', 5, 500, []),
        (r'\bast\b|sgot|aspartate', 'AST', 5, 500, []),
        (r'alkaline\s+phosphatase|\balp\b', 'ALP', 30, 1000, ['sgpt', 'sgot']),
        (r'\balbumin\b', 'Albumin', 2.0, 6.0, ['total']),
        (r'total\s+protein', 'Total Protein', 4.0, 10.0, [])
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
        numbers = re.findall(r'\b(\d+\.?\d*)\b', line)
        
        for num in reversed(numbers):
            # Skip if DIRECTLY part of a range
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
        test_line_nums = {t[3] for t in tests_found}
        start_line = tests_found[0][3]
        end_line = tests_found[-1][3] + 3
        
        next_line_values = []
        for i in range(start_line, min(end_line, len(lines))):
            if i in test_line_nums:
                continue
            
            line = lines[i]
            if len(line) < 30:
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
