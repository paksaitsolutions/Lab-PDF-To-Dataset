import re

# Test the updated regex patterns
test_text = """Patient Name:                                Registration Location:
Safia Bibi .                                 CC JINNAH HOSPITAL LHR

Age/Sex:                                     Registration Date:
73 Yr(s) / Female                            23-Feb-2024 12:42 pm
"""

def extract_basic_info(text):
    print("DEBUG: Text to parse:")
    print(repr(text[:500]))
    
    # Pattern 1: Name on next line after "Patient Name:"
    name = re.search(r"Patient\s*Name\s*:[^\n]*\n\s*([A-Za-z\s\.]+?)(?:\s{2,}|\n)", text, re.IGNORECASE)
    print(f"DEBUG: Name match (pattern 1): {name.group(1) if name else 'None'}")
    
    if not name:
        # Pattern 2: Name on same line
        name = re.search(r"Patient\s*Name\s*:\s*([A-Za-z\s\.]+?)(?:\s{2,}|\n)", text, re.IGNORECASE)
    if not name:
        name = re.search(r"Name\s*:?\s*([A-Za-z\s\.]+?)(?:\n|Registration|Lab|Age|Sample|$)", text, re.IGNORECASE)
    
    # Pattern 1: Age/Sex on next line
    age_sex_line = re.search(r"Age/Sex\s*:[^\n]*\n\s*([^\n]+)", text, re.IGNORECASE)
    print(f"DEBUG: Age/Sex line match: {age_sex_line.group(1) if age_sex_line else 'None'}")
    
    if age_sex_line:
        # Extract age and gender from the captured line
        age_match = re.search(r"(\d+)\s*Yr\(s\)\s*/\s*(Male|Female)", age_sex_line.group(1), re.IGNORECASE)
        if age_match:
            age = age_match.group(1)
            gender = age_match.group(2)
        else:
            age = ""
            gender = ""
    else:
        # Try other patterns
        age_sex = re.search(r"Age\s*/\s*Sex\s*:?\s*(\d+)\s*Years?.*?/\s*(Male|Female)", text, re.IGNORECASE)
        if not age_sex:
            age_sex = re.search(r"Age[/\s]*Sex\s*:?\s*(\d+)\s*Year.*?(Male|Female)", text, re.IGNORECASE)
        if not age_sex:
            age_sex = re.search(r"Age\s*:?\s*(\d+).*?(Male|Female)", text, re.IGNORECASE)
        
        if age_sex:
            age = age_sex.group(1)
            gender = age_sex.group(2)
        else:
            age = ""
            gender = ""

    # Clean up name
    if name:
        name_text = name.group(1).strip()
        print(f"DEBUG: Name before clean: '{name_text}'")
        # Remove trailing period and extra spaces
        name_text = name_text.rstrip('.').strip()
    else:
        name_text = ""

    return {
        "Name": name_text,
        "Age": age,
        "Gender": gender
    }

result = extract_basic_info(test_text)
print("Extracted Patient Info:")
print(f"Name: {result['Name']}")
print(f"Age: {result['Age']}")
print(f"Gender: {result['Gender']}")
