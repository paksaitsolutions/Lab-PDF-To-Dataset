import re

text = """Total RBC                4 - 6              x10^12/l      3.2"""

# Better pattern - look for the last number after the unit
pattern = r'(?:Total\s+)?(?:Red Blood Cell|RBC).*?[x\*]10\^?\d+/l\s+([0-9]+\.?[0-9]*)'
match = re.search(pattern, text, re.IGNORECASE)
print(f"Pattern match: {match}")
if match:
    print(f"Extracted value: {match.group(1)}")
