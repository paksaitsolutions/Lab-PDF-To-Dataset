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

    def extract_value(test_name):
        match = re.search(rf'{test_name}.*?(?=\n|$)', text, re.IGNORECASE | re.DOTALL)
        if not match:
            return ""
        
        line = match.group(0)
        
        # Simple logic: Get the LAST number on the line (usually the result)
        numbers = re.findall(r'([0-9]+\.?[0-9]*)', line)
        return numbers[-1] if numbers else ""
    
    data['Urea'] = extract_value(r'Urea')
    data['BUN'] = extract_value(r'BUN')
    data['Creatinine'] = extract_value(r'Creatinine')
    
    # GFR: Simple logic - find "mL/min" and get number before it
    gfr_match = re.search(r'(?:Glomerular\s+Filtration|GFR).*?(?=\n|$)', text, re.IGNORECASE | re.DOTALL)
    if gfr_match:
        gfr_line = gfr_match.group(0)
        
        # Find "mL/min" position
        ml_pos = gfr_line.lower().find('ml/min')
        if ml_pos > 0:
            # Get text before mL/min
            before_unit = gfr_line[:ml_pos]
            # Get text after mL/min
            after_unit = gfr_line[ml_pos+6:]
            
            # Extract numbers from before unit
            before_nums = re.findall(r'(\d+)', before_unit)
            # Extract numbers from after unit
            after_nums = re.findall(r'(\d+)', after_unit)
            
            # Logic: If there's a number after unit and it's > 10, use it
            # Otherwise use last number before unit
            if after_nums:
                # Get first number after unit that's > 10 and < 1000
                # Skip numbers that are part of decimals (preceded by .)
                for i, num in enumerate(after_nums):
                    if 10 < int(num) < 1000:
                        # Check if this number is part of a decimal like "1.73"
                        num_pos = after_unit.find(num)
                        if num_pos > 0 and after_unit[num_pos-1] == '.':
                            continue  # Skip, it's part of a decimal
                        data['GFR'] = num
                        break
            
            if not data.get('GFR') and before_nums:
                # Use last number before unit that's > 10 and < 1000
                for num in reversed(before_nums):
                    if 10 < int(num) < 1000:
                        data['GFR'] = num
                        break
        
        if not data.get('GFR'):
            data['GFR'] = ""
    else:
        data['GFR'] = ""
    
    data['Uric Acid'] = extract_value(r'Uric\s+Acid')

    return data
